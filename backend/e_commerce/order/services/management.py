from django.db import transaction
from financeops.models import FinancialRecord, MoneyTransferRequest, Wallet
from product.models import ProductVariant
from rest_framework import serializers

from order.models import Order, OrderItem


def process_order_creation(validated_data: dict) -> Order:
    """
    When a new order needs to be created based off on user's current cart,
    the following steps will be executed in order when calling this function:

    1) Create an unsaved instance of `Order`.
    2) By using the `Cart` object from passed in `validated_data`, validate each `CartItem` instance having
    a valid quantity.
    3) For each `CartItem`, create an unsaved `OrderItem` instance using the `Order`
    instance created in step 1.
    4) For each `CartItem`, update its associated `ProductVariant` reserved stocks and
    on hand stocks fields.
    5) Delete user's current cart items.

    The key `order` in passed in arg `validated_data` should be an instance of order
    which hasn't been saved to the database, yet.
    Note that the DB operations will all be executed in a single block using
    a transaction operation.
    """
    assert
    user = validated_data.get("user")
    order = Order(
        status=Order.UNPAID,
        customer=user,
        customer_address=validated_data["customer_address"],
        customer_notes=validated_data["notes"],
    )

    product_variants = []
    order_items = []

    with transaction.atomic():
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

        # db operations
        order.save()
        ProductVariant.objects.bulk_update(product_variants, ["reserved_stock"])
        OrderItem.objects.bulk_create(order_items)
        user.cart.items.all().delete()

    return order


def pay_order_using_wallet(wallet: Wallet, order: Order) -> FinancialRecord:
    """
    Pay an order using wallet's currency, update the order's related field
    and create a `Transaction` instance.
    """
    order_total_price = order.get_total_price()
    if wallet.balance < order_total_price:
        raise serializers.ValidationError(
            "Wallet's balance is not sufficient for paying the order."
        )
    with transaction.atomic():
        order.status = Order.PAID
        wallet.balance -= order_total_price
        transaction_obj = FinancialRecord.objects.create(
            wallet=wallet,
            type=FinancialRecord.WALLET_PAYMENT,
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

    with transaction.atomic():
        # Update the order item's product variant stocks and the order's fields.
        product_variants = []
        for item in order.items.all():
            item.product_variant.reserved_stock -= item.quantity
            item.product_variant.on_hand_stock -= item.quantity
            product_variants.append(item.product_variant)
        order.status = Order.SHIPPED
        order.tracking_code = new_tracking_code
        ProductVariant.objects.bulk_update(
            product_variants, ["reserved_stock", "on_hand_stock"]
        )
        order.save()
    return order


def update_order_to_cancelled(order: Order, validated_data: dict) -> FinancialRecord:
    """
    Only usable for order instances where the status is PAID or
    PROCESSING.

    When an order is going to be cancelled by the seller, a cancellation
    reason should be provided.

    `reserved_stock` field of the `Order` instance which was modified by the
    order will be reset back to its pre-order value.

    The refund method is based on whether the order was paid using
    wallet or direct payment:
    - If the payment method was direct payment, then a `MoneyTransferRequest`
    instance will also be created, which customer support should handle the
    refund using this instance.
    - If the payment method was wallet payment, then the wallet balance will
    be reverted back to its pre-purchase value.
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
    product_variant_items = []
    for item in order.items.all():
        item.product_variant.reserved_stock -= item.quantity
        product_variant_items.append(item.product_variant)
    order.status = Order.CANCELLED
    order.cancel_reason = new_cancel_reason
    order.cancelled_by = Order.SELLER
    trans_obj = FinancialRecord.objects.filter(
        order=order,
        type__in=[FinancialRecord.DIRECT_PAYMENT, FinancialRecord.WALLET_PAYMENT],
    ).first()
    if not trans_obj:
        raise serializers.ValidationError(
            "No associated transaction was found for this order. "
            "Please open a support ticket with order ID included."
        )

    with transaction.atomic():
        if trans_obj.type == FinancialRecord.WALLET_PAYMENT:
            customer_wallet = order.customer.wallet
            order_total_price = order.get_total_price()
            customer_wallet.balance += order_total_price
            refund_tran_obj = FinancialRecord.objects.create(
                type=FinancialRecord.WALLET_REFUND,
                amount=order_total_price,
                wallet=trans_obj.wallet,
                order=trans_obj.order,
            )
        else:
            MoneyTransferRequest.objects.create(
                requested_by=order.customer,
                amount=order.amount,
            )
            refund_tran_obj = FinancialRecord.objects.create(
                type=FinancialRecord.DIRECT_REFUND,
                amount=order_total_price,
                order=trans_obj.order,
            )
        ProductVariant.objects.bulk_update(product_variant_items, ["reserved_stock"])
        order.save()
        customer_wallet.save()
    return refund_tran_obj
