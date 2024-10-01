import logging
from typing import Union

from rest_framework import serializers
from zibal.client import ZibalIPGClient

from ecom_user.models import EcomUser
from ecom_user_profile.models import CustomerAddress, Transaction
from product.models import ProductVariant
from order.models import Cart, CartItem, Order, OrderItem
from order.tasks import cancel_unpaid_order, process_payment

from backend.e_commerce.order.services import (
    initiate_order_payment,
    create_order,
    validate_cart_not_empty,
    validate_no_on_going_orders,
)

logger = logging.getLogger("order")


class CartItemSerializer(serializers.ModelSerializer):
    """
    Intended for creating, updating and reading a cart item instance.

    Current authenticated user should be passed as context to this
    serializer with the kwarg 'user', when calling .save().
    """

    price = serializers.IntegerField(source="product_variant.price", read_only=True)
    name = serializers.IntegerField(source="product_variant.name", read_only=True)
    image = serializers.ImageField(source="product_variant.image", read_only=True)
    available_stock = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "product_variant",
            "quantity",
            "variant_price",
            "variant_name",
            "variant_image",
            "available_stock",
        ]
        extra_kwargs = {
            "cart": {"read_only": True},
            "product_variant": {"required": True},
        }

    def validate(self, attrs):
        current_user = self.context.get("user")
        if not current_user:
            raise RuntimeError(
                "User must be provided using 'user' kwarg when calling .save()"
            )
        self._run_cart_item_validations(attrs, current_user)
        return attrs

    def create(self, validated_data):
        current_user = self.context.get("user")
        cart = Cart.objects.get_or_create(user=current_user)
        validated_data["cart"] = cart.id
        return super().create(validated_data)

    def _run_cart_item_validations(self, attrs: dict, current_user: EcomUser) -> None:
        selected_variant = ProductVariant.objects.get(id=attrs["product_variant"])
        self._validate_same_seller(selected_variant, attrs)
        self._validate_availability(selected_variant)
        self._validate_quantity(selected_variant, attrs)
        self._validate_active_seller(selected_variant)
        self._validate_seller_is_not_current_user(selected_variant, current_user)

    def _validate_same_seller(
        self, selected_variant: ProductVariant, attrs: dict
    ) -> None:
        cart_item = CartItem.objects.filter(cart_id=attrs["cart"]).first()
        if cart_item:
            if selected_variant.owner != cart_item.product_variant.owner:
                raise serializers.ValidationError(
                    "Cart items should belong to only one seller"
                )

    def _validate_availability(self, selected_variant: ProductVariant) -> None:
        if not selected_variant.is_available:
            raise serializers.ValidationError(
                "The selected product doesn't have any available stocks"
            )

    def _validate_quantity(self, selected_variant: ProductVariant, attrs: dict) -> None:
        if attrs["quantity"] > selected_variant.available_stock:
            raise serializers.ValidationError(
                "The quantity of selected product cannot be higher than the product's available stock"
            )

    def _validate_active_seller(selected_variant: ProductVariant) -> None:
        if not selected_variant.owner.is_verified:
            raise serializers.ValidationError(
                "The selected product cannot be added to cart due to seller's account being inactive"
            )

    def _validate_seller_is_not_current_user(
        selected_variant: ProductVariant, current_user: EcomUser
    ) -> None:
        if selected_variant.owner != current_user:
            raise serializers.ValidationError(
                "Cannot add items from the user's own shop to the cart!"
            )


class CartSerializerForCustomer(serializers.ModelSerializer):
    """
    This serializer is intended only for representation or read only operations,
    so it shouldn't be used for create/update operations.
    """

    items = CartItemSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]
        extra_kwargs = {
            "user": {"read_only": True},
        }


class OrderItemSerializer(serializers.ModelSerializer):
    """
    This serializer is only intended for read only operations.
    Since the order items creation are handled by server by using the user's current cart
    items. It is assumed that the cart items have already been validated, though some
    other validations are processed in the OrderSerializer.

    Since the price of the product can be changed in the future, so
    """

    name = serializers.IntegerField(source="product_variant.name", read_only=True)
    image = serializers.ImageField(source="product_variant.image", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "submitted_price",
            "name",
            "image",
            "product_variant",
            "quantity",
        ]
        extra_kwargs = {
            "order": {"read_only": True},
            "product_variant": {"required": True},
        }


class OrderSerializerForCustomer(serializers.ModelSerializer):
    """
    Updating order by the customer is only permitted if the order is still
    in UNPAID state.
    """

    items = OrderItemSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()
    payment_link = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "items",
            "customer_address",
            "notes",
            "payment_service",
            "seller",
            "payment_link",
        ]
        extra_kwargs = {
            "status": {"read_only": True},
            "user": {"read_only": True},
        }

    def get_seller(self, order_obj: Order) -> Union[int, None]:
        order_item = order_obj.items.first()
        if order_item:
            return order_item.owner
        return None

    def get_payment_link(self, order: Order) -> Union[str, None]:
        if order.payment_track_id and not order.paid_amount:
            return ZibalIPGClient.create_payment_link(order.payment_track_id)
        return None

    def validate(self, attrs):
        request_method = self.context["request"].method
        if request_method in ("PUT", "PATCH"):
            if self.instance.status not in (Order.UNPAID, Order.ONHOLD):
                raise serializers.ValidationError(
                    "Orders cannot be modified by the customer after they have been paid."
                )
        user = self.context.get("user")
        if not user:
            raise RuntimeError(
                "The user must be passed using 'user' kwarg when calling .save() method"
            )
        # assigned customer address should belong  to current user
        customer_address_obj = CustomerAddress.objects.get(attrs["customer_address"])
        if customer_address_obj.user != attrs["user"]:
            raise serializers.ValidationError(
                "The given customer address does not belong to this user"
            )
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        validate_cart_not_empty(user)
        validate_no_on_going_orders(user)
        order = create_order(validated_data)
        order = initiate_order_payment(order)
        # cancel the order if not paid after 1 hour
        cancel_unpaid_order.apply_async(args=(order.id), countdown=60 * 60)
        # will check after 20 minutes
        process_payment.apply_async(
            args=(order.payment_track_id, order.id), countdown=60 * 20
        )
        return order


class OrderSerializerForSeller(serializers.ModelSerializer):
    """
    Allows the following write operations for sellers:

    - Updating the order's status with the following constraints: (the backend app
    should also execute the necessary changes to the order such as updating the
    product's stocks when the order status gets changed):
        - Seller Should input a tracking code when changing the status to SHIPPED.
        - Seller Should input a cancellation reason when changing the status to
        CANCELLED. In result, the server will refund the money back to the customer.
    """

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "created_at",
            "status",
            "items",
            "customer_address",
            "notes",
            "paid_amount",
            "tracking_code",
            "cancel_reason",
        ]
        read_only_fields = [
            "user",
            "created_at",
            "customer_address",
            "notes",
            "paid_amount",
        ]

    def update(self, order, validated_data):
        new_status = validated_data.get("status")
        if new_status not in (
            Order.PROCESSING,
            Order.SHIPPED,
            Order.CANCELLED,
        ):
            raise serializers.ValidationError(
                "The vendor can only change the status of an order to one of "
                "the following states: Processing, Shipped or Cancelled"
            )

        if new_status == Order.SHIPPED:
            if not validated_data.get("tracking_code") or order.tracking_code:
                raise serializers.ValidationError(
                    "A tracking code should be provided when updating the status to shipped"
                )
            order_items = []
            for item in order.items.all():
                item.product_variant.reserved_stock -= item.quantity
                item.product_variant.on_hand_stock -= item.quantity
                order_items.append(item)
            OrderItem.objects.bulk_update(
                order_items, ["reserved_stock", "on_hand_stock"]
            )
        if new_status == Order.CANCELLED:
            if not validated_data.get("cancel_reason"):
                raise serializers.ValidationError(
                    "A cancellation reason should be provided when changing the status to cancelled"
                )
            order_items = []
            for item in order.items.all():
                item.product_variant.reserved_stock -= item.quantity
                order_items.append(item)
            OrderItem.objects.bulk_update(order_items, ["reserved_stock"])

        return super().update(order, validated_data)
