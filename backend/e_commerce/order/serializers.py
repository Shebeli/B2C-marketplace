import logging
from typing import Union

from rest_framework import serializers
from zibal.client import ZibalIPGClient

from ecom_user.models import EcomUser
from ecom_user_profile.models import CustomerAddress
from product.models import ProductVariant
from order.models import Cart, CartItem, Order, OrderItem
from order.tasks import cancel_unpaid_order, process_payment

from order.services import (
    initiate_order_payment,
    create_order,
    update_order_to_cancelled,
    update_order_to_shipped,
)

logger = logging.getLogger("order")


class CartItemSerializer(serializers.ModelSerializer):
    """
    Intended for creating, updating and reading a cart item instance by
    a customer.

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

    def to_internal_value(self, data):
        current_user = self.context.get("user")
        if not current_user:
            raise RuntimeError(
                "User must be provided using 'user' kwarg when calling .save()"
            )
        cart = Cart.objects.get_or_create(user=current_user)
        data["cart"] = cart.id
        return super().to_internal_value(data)

    def validate(self, attrs):
        current_user = self.context.get("user")
        if not current_user:
            raise RuntimeError(
                "User must be provided using 'user' kwarg when calling .save()"
            )
        self._run_cart_item_validations(attrs, current_user)
        return attrs

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
    This serializer is intended only for representation, and to be read only
    by the customer.
    """

    items = CartItemSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def get_seller(self, cart: Cart) -> Union[int, None]:
        seller = cart.get_seller()
        if not seller:
            return None
        return seller.id


class OrderItemSerializer(serializers.ModelSerializer):
    """
    This serializer is only intended for representation, accessed only by
    its customer and the seller.

    When creating the order, the `OrderItem` instances creation are handled
    by server by using the user's current cart items.

    It is assumed that the cart items have already been validated
    (such as item availiblity, proper quantity, and so on), though some
    other related validations are processed in the `OrderSerializer`.
    """

    name = serializers.CharField(source="product_variant.name", read_only=True)
    image = serializers.ImageField(source="product_variant.image", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "submitted_price",
            "quantity",
            "name",
            "image",
            "product_variant",
        ]


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ["id", "address"]


class OrderSerializerForCustomer(serializers.ModelSerializer):
    """
    Intended to be accessed and used by the customer of an order.

    Updating order's fields such as customer notes by the customer is only
    permitted if the order is still in `UNPAID` state.

    Customer should proceed to pay the order either using direct payment
    or using their wallet. If the chosen method is direct payment, then
    an instance of `Payment` will be created and will keep track of the
    customer's latest IPG payment attempt.
    """

    items = OrderItemSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()
    payment_link = serializers.SerializerMethodField()
    selected_address = CustomerAddressSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "items",
            "selected_address",
            "notes",
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
        payment_obj = order.payment
        if not payment_obj:
            return None
        if payment_obj.is_payment_link_expired:
            return None
        return ZibalIPGClient.create_payment_link(payment_obj.track_id)

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
        self._validate_address(attrs)
        self._validate_cart_not_empty(user)
        self._validate_no_on_going_orders(user)
        return attrs

    def create(self, validated_data):
        order = create_order(validated_data)
        # initiate_order_payment(order)
        # cancel the order if it isn't paid after 1 hour
        cancel_unpaid_order.apply_async(args=(order.id), countdown=60 * 60)
        # Check the order's status and verify the payment on the IPG server if it is not so.
        # process_payment.apply_async(
        #     args=(order.payment_track_id, order.id), countdown=60 * 20
        # )
        return order

    def _validate_address(attrs: dict) -> None:
        customer_address_obj = CustomerAddress.objects.get(attrs["customer_address"])
        if customer_address_obj.user != attrs["user"]:
            raise serializers.ValidationError(
                "The given customer address does not belong to this user"
            )

    def _validate_cart_not_empty(user: EcomUser) -> None:
        """Cart shouldn't be empty when requesting a new order."""
        if not user.cart.items.exists():
            raise serializers.ValidationError("The cart doesn't contain any items")

    def _validate_no_on_going_orders(user: EcomUser) -> None:
        """
        Validates no ongoing order should exist with the same seller when
        requesting a new order.
        """
        on_going_order_statuses = (Order.PENDING, Order.PROCESSING, Order.SHIPPED)
        seller = user.cart.items.first().owner
        if user.orders.filter(
            seller=seller, status__in=on_going_order_statuses
        ).exists():
            raise serializers.ValidationError(
                "Cannot create a new order since an order is already on going with the same seller"
            )


class OrderSerializerForSeller(serializers.ModelSerializer):
    """
    Allows the following write operations for sellers:

    - Updating the order's status with the following constraints: (the server
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
            update_order_to_shipped(order, validated_data)
        if new_status == Order.CANCELLED:
            update_order_to_cancelled(order, validated_data)
        return super().update(order, validated_data)
