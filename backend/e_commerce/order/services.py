import logging

from django.db import transaction
from ecom_user.models import EcomUser
from rest_framework import serializers
from zibal.exceptions import RequestError, ResultError
from zibal.client import ZibalIPGClient
from order.models import Order, OrderItem
from django.conf import settings
from django.urls import reverse
from product.models import ProductVariant

logger = logging.getLogger("order")


def initiate_order_transaction(order: Order) -> None:
    """
    Initialize a zibal IPG client, request a new transaction using the initialized
    client and if the request is successful, save the payment track id to the
    order instance.
    """
    client = ZibalIPGClient(
        settings.ZIBAL_MERCHANT, raise_on_invalid_result=True, logger=logger
    )
    try:
        request_data = client.request_transaction(
            amount=order.get_total_price(),
            callback_url=reverse("payment-callback"),
            order_id=order.id,
            mobile=order.user.phone,
        )
    except RequestError:
        # ZibalIPGClient uses logging to log network error
        return serializers.ValidationError(
            "A network error occured when working with payment service, please try again later"
        )
    except ResultError as exc:
        logger.exception(f"An unexpected `result` was received from the IPG: {exc}")
        return serializers.ValidationError(
            "An unexpected result was received from the payment gateway service."
        )
    order.payment_track_id = request_data.track_id
    order.save()


def validate_and_proceed_cart_items(order: Order) -> None:
    """
    The passed in argument `order` should be an instance of order which hasn't
    been saved to the database, yet.

    When a new order needs to be created based on the user's current cart,
    the following steps should be executed in order using this method:
    1) Validate each cart item in terms of stock availablity and having a valid quantity.
    2) For each cart item, create an order item.
    3) For each cart item's product variant, update reserved stocks and available stocks.
    5) Delete user's current cart items.
    4) Save all the changes made above to the database using atomic transaction method.

    """
    user = order.user
    product_variants = []
    order_items = []
    for item in user.cart.items.all():
        if not item.product_variant.is_available:
            raise serializers.ValidationError(
                f"The product {item.product_variant.name} doesn't have any available stocks"
            )
        if item.quantity > item.product_variant.available_stock:
            raise serializers.ValidationError(
                f"The selected product {item.product_variant.name} quantity cannot be higher than product's available stock"
            )

        order_item = OrderItem(
            order=order,
            product_variant=item.product_variant,
            submitted_price=item.product_variant.price,
            quantity=item.quantity,
        )
        product_variant = item.product_variant
        product_variant.reserved_stock += item.quantity

        order_items.append(order_item)
        product_variants.append(product_variant)

    with transaction.atomic():
        order.save()
        ProductVariant.objects.bulk_update(
            product_variants, ["on_hand_stock", "reserved_stock"]
        )
        OrderItem.objects.bulk_create(order_items)
        user.cart.items.all().delete()


def validate_cart_not_empty(user: EcomUser) -> None:
    """Cart shouldn't be empty when requesting a new order."""
    if not user.cart.items.exists():
        raise serializers.ValidationError("The cart doesn't contain any items")


def validate_no_on_going_orders(user: EcomUser) -> None:
    """No ongoing order should exist with the same seller when requesting a new order."""
    on_going_order_statuses = (Order.PENDING, Order.PROCESSING, Order.SHIPPED)
    seller = user.cart.items.first().owner
    if user.orders.filter(seller=seller, status__in=on_going_order_statuses).exists():
        raise serializers.ValidationError(
            "Cannot create a new order since an order is already on going with the same seller"
        )
