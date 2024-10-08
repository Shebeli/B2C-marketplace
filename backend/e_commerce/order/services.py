import logging

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from rest_framework import serializers
from zibal.client import ZibalIPGClient
from zibal.exceptions import RequestError, ResultError
from zibal.models.schemas import TransactionRequireResponse

from product.models import ProductVariant
from wallet.models import Transaction, Wallet, Payment
from ecom_user.models import EcomUser
from order.models import Order, OrderItem

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


def initiate_ipg_payment(amount: int) -> TransactionRequireResponse:
    client = ZibalIPGClient(
        settings.ZIBAL_MERCHANT, raise_on_invalid_result=True, logger=logger
    )
    try:
        request_data = client.request_transaction(
            amount=amount,
            callback_url=reverse("payment-callback"),
        )
    except RequestError:
        # ZibalIPGClient uses logging to log network error
        raise serializers.ValidationError(
            "A network error occured when working with payment service, please try again later"
        )
    except ResultError:
        # logger.exception(f"An unexpected `result` was received from the IPG: {exc}")
        raise serializers.ValidationError(
            "An unexpected result was received from the payment gateway service."
        )
    return request_data


def inititate_wallet_payment(wallet: Wallet, amount: int) -> Transaction:
    """
    Initialize an IPG payment, update the order's status to PAYING
    and createa `Payment` instance.
    """
    request_data = initiate_ipg_payment(amount=amount)
    payment = Payment.objects.create(
        wallet=wallet,
        amount=amount,
        service_name="Zibal",
        status=Payment.PAYING,
        track_id=request_data.track_id,
    )
    return payment


def initiate_order_payment(order: Order) -> Payment:
    """
    Initialize an IPG payment, update the order's status to PAYING
    and createa `Payment` instance.
    """
    request_data = initiate_ipg_payment(amount=order.amount)
    order.status = Order.PAYING
    with transaction.atomic():
        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            service_name="Zibal",
            status=Payment.PAYING,
            track_id=request_data.track_id,
        )
        order.save()
    return payment


def finalize_order_payment(payment: Payment) -> Transaction:
    """
    The passed in `Payment` instance should already be in PAID
    status. if so, then the order's status will be updated to PAID status
    with appropriate changes. Otherwise, an error will be raised.
    """
    order = payment.order
    if not order:
        raise ValueError("The payment has no order associated with it")
    if payment.status != Payment.PAID:
        raise ValueError("The payment hasn't been paid")
    if order.status != Order.PAYING:
        raise ValueError("The given order instance should be in PAYING state")
    with transaction.atomic():
        order.status = order.PAID
        order.save()
        tran = Transaction.objects.create(
            amount=order.total_price,
            type=Transaction.DIRECT_PAYMENT,
            order=order,
        )
    return tran


def finalize_wallet_payment(payment: Payment) -> Transaction:
    """
    The passed in `Payment` instance should already be in PAID status.
    if so, then the wallet's balance will increased.
    """
    wallet = payment.wallet
    if not wallet:
        raise ValueError("The payment instance has no wallet associated with it")
    if payment.status != Payment.PAID:
        raise ValueError("The payment hasn't been paid")
    if payment.is_used:
        raise ValueError("The payment has already been verified")

    with transaction.atomic():
        wallet.balance += payment.amount
        wallet.save()
        tran = Transaction.objects.create(
            amount=payment.amount, type=Transaction.DEPOSIT, wallet=wallet
        )
    return tran


def pay_order_using_wallet(wallet: Wallet, order: Order) -> Transaction:
    """
    Pay an order using wallet's currency, update the order's related field
    and create a `Transaction` instance.
    """
    if wallet.balance < order.total_price:
        raise serializers.ValidationError(
            "Wallet's balance is not sufficient for paying the order"
        )
    wallet.balance -= order.total_price
    order.status = Order.PAID
    with transaction.atomic():
        transaction_obj = Transaction.objects.create(
            wallet=wallet,
            type=Transaction.WALLET_PAYMENT,
            amount=order.get_total_price(),
            order=order,
        )
        order.save()
        wallet.save()
    return transaction_obj


def update_order_to_shipped(order: Order, validated_data: dict) -> Order:
    """
    Updates the order's status to SHIPPED with the following changes:
    The order's items stocks will be updated accordingly, and the
    order's tracking code either will be set and the order's status
    will also be updated to SHIPPED.

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


def update_order_to_cancelled(order: Order, validated_data: dict) -> Transaction:
    """
    When an order is going to be cancelled by the seller, a cancellation
    reason should be provided.

    Both `on_hand_stock` and `reserved_stock` which were changed by
    the order will be reset back to pre-order state.

    The refund method is based on whether the order was paid using
    wallet or direct payment:
    - If the payment method was direct payment, then a
    `MoneyTransferRequest` instance will also be created,
    which customer support should do the money transfer.
    - If the payment method was wallet payment, then
    the wallet balance will be increased to the prior
    amount.

    In both cases, a `Transaction` instance will be created.
    """
    new_cancel_reason = validated_data.get("cancel_reason")
    if not new_cancel_reason:
        raise serializers.ValidationError(
            "A cancellation reason should be provided when cancelling the order."
        )
    if order.status == Order.CANCELLED:
        order.cancel_reason = new_cancel_reason
        order.save()
        return order

    if order.status not in (Order.PAID, Order.PROCESSING):
        raise serializers.ValidationError(
            "Order cannot be cancelled if it is not in PAID or PROCESSING state."
        )
    order_items = []
    for item in order.items.all():
        item.product_variant.reserved_stock -= item.quantity
        item.product_variant.on_hand_stock += item.quantity
        order_items.append(item)
    order.status = Order.CANCELLED
    order.cancel_reason = new_cancel_reason
    order.cancelled_by = Order.SELLER
    trans_obj = Transaction.objects.filter(
        order=order, type__in=[Transaction.DIRECT_PAYMENT, Transaction.WALLET_PAYMENT]
    ).first()
    if not trans_obj:
        raise serializers.ValidationError(
            "No associated transaction was found for this order. "
            "Please open a support ticket with order ID included."
        )

    with transaction.atomic():
        if trans_obj.type == Transaction.WALLET_PAYMENT:
            customer_wallet = order.customer.wallet
            customer_wallet.balance += order.total_price
            refund_tran_obj = Transaction.objects.create(
                type=Transaction.WALLET_REFUND,
                amount=order.total_price,
                wallet=trans_obj.wallet,
                order=trans_obj.order,
            )
        else:
            refund_tran_obj = Transaction.objects.create(
                type=Transaction.DIRECT_REFUND,
                amount=order.total_price,
                order=trans_obj.order,
            )
        OrderItem.objects.bulk_update(order_items, ["reserved_stock"])
        order.save()
        customer_wallet.save()
    return refund_tran_obj


