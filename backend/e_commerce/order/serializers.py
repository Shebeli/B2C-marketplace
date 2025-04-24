import logging
from typing import Union
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from ecom_user_profile.models import CustomerAddress
from financeops.models import FinancialRecord, Payment
from rest_framework import serializers
from zibal.client import ZibalIPGClient
from zibal.response_codes import STATUS_CODES

from order.models import Cart, CartItem, Order, OrderItem
from order.services.management import (
    CartService,
)
from order.services.payment import initiate_order_payment
from order.services.validators import (
    validate_order_is_not_finished,
)
from order.tasks import cancel_unpaid_order

logger = logging.getLogger("order")


class CartItemSerializer(serializers.ModelSerializer):
    """
    Intended for creating, updating and reading a cart item instance by
    a customer. (For update operations, updating the field `product_variant`
    is not allowed.)

    Current authenticated user should be passed as context to this
    serializer with the kwarg 'user', when calling .save().
    """

    variant_price = serializers.IntegerField(
        source="product_variant.price", read_only=True
    )
    variant_name = serializers.IntegerField(
        source="product_variant.name", read_only=True
    )
    variant_image = serializers.ImageField(
        source="product_variant.product.main_variant.image", read_only=True
    )
    is_available = serializers.IntegerField(
        source="product_variant.is_available", read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_variant",
            "quantity",
            "variant_price",
            "variant_name",
            "variant_image",
            "is_available",
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
        return super().to_internal_value(data)

    def validate(self, attrs):
        current_user = self.context.get("user")
        if not current_user:
            raise RuntimeError(
                "User must be provided using 'user' kwarg when calling .save()"
            )
        return attrs

    def create(self, validated_data):
        return CartService.add_item_to_cart(
            validated_data["user"],
            validated_data["product_variant"],
            validated_data["quantity"],
        )

    def update(self, instance, validated_data):
        if validated_data["product_variant"]:
            if instance.product_variant.id != validated_data["product_variant"]:
                raise serializers.ValidationError("Product variant cannot be modified.")
        return super().update(self, instance, validated_data)


class CartSerializerForCustomer(serializers.ModelSerializer):
    """
    This serializer is intended only for read-only purposes used by the
    customers.
    """

    items = CartItemSerializer(many=True, read_only=True)
    seller = serializers.SerializerMethodField()
    errors = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "seller", "user", "items", "errors"]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def get_seller(self, cart: Cart) -> Union[int, None]:
        seller = cart.get_seller()
        return seller.id if seller else None

    def get_errors(self, cart: Cart) -> dict:
        return CartService.get_user_cart_errors(cart.user)


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
        read_only_fields = ["status", "user", "seller"]

    def get_payment_link(self, order: Order) -> Union[str, None, dict]:
        payment_obj = order.payment
        if not payment_obj:
            return {"code": -1, "detail": _("No ")}
        if payment_obj.is_payment_link_expired:
            return {"code": -2, "detail": _("Payment link is expired.")}
        return ZibalIPGClient.create_payment_link(payment_obj.track_id)

    def validate(self, attrs):
        user = self.context.get("user")
        if not user:
            raise RuntimeError(
                "The user must be passed using 'user' kwarg when calling .save() method"
            )
        return attrs

    def create(self, validated_data):
        order = 
        # initiate_order_payment(order)
        # cancel the order if it isn't paid after 1 hour
        cancel_unpaid_order.apply_async(args=(order.id), countdown=60 * 60)
        # Check the order's status and verify the payment on the IPG server if it is not so.
        # process_payment.apply_async(
        #     args=(order.payment_track_id, order.id), countdown=60 * 20
        # )
        return order


class OrderPaymentSerializer(serializers.Serializer):
    """
    Intended only for update operations used by the customer.

    If the selected method is direct payment, the `ipg_id` field
    should be provided (assuming the ipg service is available).
    """

    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    # either one of these two fields should be provided
    pay_with_wallet = serializers.BooleanField(allow_null=True)
    ipg_id = serializers.IntegerField(allow_null=True)

    def update(self, order: Order, validated_data: dict) -> Order:
        if order.status not in (Order.UNPAID, Order.PAYING):
            raise serializers.ValidationError(
                "The given order should be in UNPAID or PAYING status"
            )
        if validated_data["pay_with_wallet"] and validated_data["ipg_choice"]:
            raise serializers.ValidationError(
                "Only one of the fields 'pay_with_wallet' and 'ipg_choice' should be provided."
            )
        if validated_data["pay_with_wallet"]:
            transaction = pay_order_using_wallet(order.customer.wallet, order)
            return transaction
        elif validated_data["ipg_choice"]:
            ipgs = cache.get("available_ipgs")
            if validated_data["ipg_id"] not in ipgs:
                raise serializers.ValidationError(
                    "The selected IPG service is either not recognized or its disabled"
                )
            base_url = self.context.get("request").build_absolute_uri()
            payment = initiate_order_payment(order, validated_data["ipg_id"], base_url)
            return payment
        raise serializers.ValidationError(
            "One of the fields `pay_with_wallet` or `ipg_choice` should be provided."
        )

    def to_representation(self, instance: Union[Payment, FinancialRecord]):
        ret = {}
        if isinstance(instance, Payment):
            ret["payment_link"] = instance.get_payment_link()
            ret["amount"] = instance.amount
            ret["ipg_service"] = instance.ipg_service
        elif isinstance(instance, FinancialRecord):
            ret["description"] = "Order was paid succesfully using wallet."
            ret["amount"] = instance.amount
            ret["paid_at"] = instance.created_at
        return ret


class OrderSerializerForSeller(serializers.ModelSerializer):
    """
    Allows the following update operations for order objects by sellers:

    - Updating the order's status with the following constraints:
        - Seller Should input a tracking code when changing the status to SHIPPED.
        - Seller Should input a cancellation reason when changing the status to
        CANCELLED.

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
            "tracking_code",
            "cancel_reason",
        ]
        read_only_fields = [
            "user",
            "created_at",
            "customer_address",
            "notes",
        ]

    def update(self, order, validated_data):
        validate_order_is_not_finished(order)
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
        elif new_status == Order.CANCELLED:
            update_order_to_cancelled(order, validated_data)
        elif new_status == Order.PROCESSING:
            order.status = Order.PROCESSING
            order.save()
        return order


class ZibalCallbackSerializer(serializers.Serializer):
    """
    Only a placeholder for data, maybe a datastructure like dataclass
    """

    success = serializers.ChoiceField(choices=[0, 1])
    track_id = serializers.CharField()
    order_id = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=STATUS_CODES.keys())
