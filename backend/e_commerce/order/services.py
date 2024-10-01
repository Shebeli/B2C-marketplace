import logging

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from rest_framework import serializers
from zibal.client import ZibalIPGClient
from zibal.exceptions import RequestError, ResultError

from product.models import ProductVariant
from wallet.models import Transaction, Wallet
from ecom_user.models import EcomUser
from order.models import Order, OrderItem
from wallet.models import Wallet, WithdrawalRequest, Transaction, Payment

logger = logging.getLogger("order")


def create_order(validated_data: dict) -> Order:
    """
    When a new order needs to be created based on the user's current cart,
    the following steps will be executed in order using this method:
    1) Validate each cart item's stock availability and having a valid quantity.
    2) For each cart item, create an order item.
    3) For each cart item's product variant, update reserved stocks and available stocks.
    4) Delete user's current cart items.
    5) Save all the changes made above to the database using atomic transaction method.

    The passed in argument `order` should be an instance of order which hasn't
    been saved to the database, yet.
    """
    user = validated_data.get("user")
    order = Order(
        status=Order.UNPAID,
        user=user,
        customer_address=validated_data["customer_address"],
        notes=validated_data["notes"],
    )

    product_variants = []
    order_items = []
    # validate each item stock availiblity and proper quantity
    for item in user.cart.items.all():
        if not item.product_variant.is_available:
            raise serializers.ValidationError(
                f"The product {item.product_variant.name} doesn't have any available stocks"
            )
        if item.quantity > item.product_variant.available_stock:
            raise serializers.ValidationError(
                f"The selected product {item.product_variant.name} quantity cannot be higher than product's available stock"
            )

        # create order python instances and update the stocks
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
        ProductVariant.objects.bulk_update(product_variants, ["reserved_stock"])
        OrderItem.objects.bulk_create(order_items)
        user.cart.items.all().delete()

    return order


def initiate_order_payment(order: Order) -> Order:
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
            amount=order.total_price,
            callback_url=reverse("payment-callback"),
            order_id=order.id,
            mobile=order.user.phone,
        )
    except RequestError:
        # ZibalIPGClient uses logging to log network error
        raise serializers.ValidationError(
            "A network error occured when working with payment service, please try again later"
        )
    except ResultError as exc:
        logger.exception(f"An unexpected `result` was received from the IPG: {exc}")
        raise serializers.ValidationError(
            "An unexpected result was received from the payment gateway service."
        )
    order.payment_track_id = request_data.track_id
    order.status = Order.PAYING
    order.save()

    return order


def finalize_order_payment(order: Order, payment: Payment) -> Transaction:
    """
    Note that the passed in `Payment` instance should already be in PAID
    status. if so, then the order's status will be updated to PAID status
    with appropriate changes. Otherwise, appropriate error will be raised.
    """
    if payment.status != Payment.PAID:
        raise serializers.ValidationError(
            "The payment transaction hasn't been paid yet"
        )
    if order.status != Order.PAYING:
        raise serializers.ValidationError(
            "The given order instance should be in PAYING state"
        )


def pay_order_using_wallet(wallet: Wallet, order: Order) -> Transaction:
    """
    Pay an order using wallet's currency, update the order's related field
    and create a wallet transaction instance.
    """
    if wallet.balance < order.total_price:
        raise serializers.ValidationError(
            "Not enough wallet currency for the requested action"
        )
    wallet.balance -= order.total_price
    order.paid_amount = order.total_price
    order.status = Order.PAID
    with transaction.atomic():
        transaction_obj = Transaction.objects.create(
            wallet=wallet,
            type=Transaction.PAYMENT,
            amount=order.get_total_price(),
            order=order,
        )
        order.save()
        wallet.save()
    return transaction_obj


def increase_balance_with_payment(
    wallet: Wallet, amount: int, payment_track_id: int
) -> Transaction:
    """
    For increasing the balance of the given wallet via payment. Will also
    create a `Transaction` instance.
    """
    ZibalIPGClient(settings.ZIBAL_MERCHANT, raise_on_invalid_result=True, logger=logger)
    with transaction.atomic():
        wallet_transaction = Transaction.objects.create(
            wallet=wallet,
            type=Transaction.DEPOSIT,
            amount=amount,
            payment_track_id=payment_track_id,
        )
        wallet.balance += amount
        wallet.save()
    return wallet_transaction


def validate_cart_not_empty(user: EcomUser) -> None:
    """Cart shouldn't be empty when requesting a new order."""
    if not user.cart.items.exists():
        raise serializers.ValidationError("The cart doesn't contain any items")


def validate_no_on_going_orders(user: EcomUser) -> None:
    """
    Validates no ongoing order should exist with the same seller when
    requesting a new order.
    """
    on_going_order_statuses = (Order.PENDING, Order.PROCESSING, Order.SHIPPED)
    seller = user.cart.items.first().owner
    if user.orders.filter(seller=seller, status__in=on_going_order_statuses).exists():
        raise serializers.ValidationError(
            "Cannot create a new order since an order is already on going with the same seller"
        )


def update_order_to_shipped(order: Order, validated_data: dict) -> Order:
    """
    Updates the order's status to SHIPPED with the following changes:
    The order's items stocks will be updated accordingly, and the
    order's tracking code will be set or be updated and the 
    order's status will be updated.

    If the order is already in SHIPPED status when calling this function,
    only the order's tracking code will be updated.
    """
    if order.status not in (Order.PAID, Order.SHIPPED, Order.PROCESSING):
        raise serializers.ValidationError(
            "SHIPPED status update is only usable when the order is in PAID"
            ", SHIPPED or PROCESSING state."
        )
    new_tracking_code = validated_data.get("tracking_code")
    if not new_tracking_code:
        raise serializers.ValidationError(
            "A tracking code should be provided when updating the status to"
            " shipped or updating the tracking code"
        )
    
    # if the order is already updated to SHIPPED status, then the assumption is 
    # that the current call is intended for updating the order's tracking code.
    if order.tracking_code or order.status == Order.SHIPPED:
        order.tracking_code = new_tracking_code
        order.save()
        return order

    # Update the order items and the orders
    order_items = []
    for item in order.items.all():
        item.product_variant.reserved_stock -= item.quantity
        item.product_variant.on_hand_stock -= item.quantity
        order_items.append(item)
    order.status = Order.SHIPPED
    order.tracking_code = new_tracking_code

    with transaction.atomic():
        OrderItem.objects.bulk_update(order_items, ["reserved_stock", "on_hand_stock"])
        order.save()
    return order


def update_order_to_cancelled(order: Order, validated_data: dict) -> Order:
    new_cancel_reason = validated_data.get("cancel_reason")
    if not new_cancel_reason:
        raise serializers.ValidationError(
            "A cancellation reason should be provided when changing the status to cancelled"
        )
    if order.status == Order.CANCELLED:
        order.cancel_reason = new_cancel_reason
        order.save()
        return order
    if order.status not in (Order.PAID, Order.PROCESSING):
        raise serializers.ValidationError(
            "Order cannot be cancelled if the state is not PAID or PROCESSING"
        )

    order_items = []
    for item in order.items.all():
        item.product_variant.reserved_stock -= item.quantity
        order_items.append(item)
    order.status = Order.CANCELLED
    order.cancel_reason = new_cancel_reason
    order.cancelled_by = Order.SELLER
    customer_wallet = order.customer.wallet
    customer_wallet.balance += order.total_price

    with transaction.atomic():
        OrderItem.objects.bulk_update(order_items, ["reserved_stock"])
        order.save()
        customer_wallet.save()
        transaction_obj = Transaction.objects.create(
            type=Transaction.CANCELLATION,
            amount=order.total_price,
            wallet=customer_wallet,
            order=order,
        )
    return transaction_obj
