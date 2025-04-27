import pytest
from financeops.models import FinancialRecord

from order.models import Cart, CartItem, Order
from order.services.order import (
    pay_order_using_wallet,
    process_order_creation,
    update_order_to_cancelled,
    update_order_to_shipped,
)

# Note that the input data for the functions in the
# `process_order_creation` module are expected to
# be validated serializer data.


@pytest.mark.django_db
def test_process_order_creation(customer_and_seller, sample_product_instance_factory):
    customer, seller = customer_and_seller
    product = sample_product_instance_factory()

    cart_total_price = 0
    for variant in product.variants.all():
        CartItem.objects.create(
            cart=customer.cart,
            product_variant=variant,
            quantity=10,
        )
        cart_total_price += variant.price * 10
    data = {
        "user": customer,
        "notes": "ooooo",
        "customer_address": customer.customer_addresses.first(),
    }
    order = process_order_creation(data)
    product.refresh_from_db()
    # check the order and the cart
    assert dict(customer.cart.items.all()) == {}
    assert order.status == Order.UNPAID
    assert order.customer_address == customer.customer_addresses.first()
    assert order.customer_notes == data["notes"]
    assert order.get_total_price() == cart_total_price

    # check the updated stocks
    variant_1 = product.variants.first()
    variant_2 = product.variants.last()
    assert variant_1.reserved_stock == 10
    assert variant_2.reserved_stock == 10


@pytest.mark.django_db
def test_pay_order_using_wallet(customer_and_seller, sample_product_instance_factory):
    customer, seller = customer_and_seller
    product = sample_product_instance_factory()
    for variant in product.variants.all():
        CartItem.objects.create(
            cart=customer.cart,
            product_variant=variant,
            quantity=10,
        )
    data = {
        "user": customer,
        "notes": "ooooo",
        "customer_address": customer.customer_addresses.first(),
    }
    pre_payment_wallet_balance = customer.wallet.balance
    order = process_order_creation(data)
    transaction_obj = pay_order_using_wallet(customer.wallet, order)
    order.refresh_from_db()

    assert order.status == Order.PAID
    assert (
        customer.wallet.balance + order.get_total_price() == pre_payment_wallet_balance
    )

    assert transaction_obj.type == FinancialRecord.WALLET_PAYMENT
    assert transaction_obj.amount == order.get_total_price()
    assert transaction_obj.order == order


@pytest.mark.django_db
def test_updating_order_to_shipped(
    customer_and_seller, sample_product_instance_factory
):
    # prepare the data
    customer, seller = customer_and_seller
    product = sample_product_instance_factory()
    for variant in product.variants.all():
        CartItem.objects.create(
            cart=customer.cart,
            product_variant=variant,
            quantity=10,
        )
    data = {
        "user": customer,
        "notes": "ooooo",
        "customer_address": customer.customer_addresses.first(),
    }
    order = process_order_creation(data)
    pay_order_using_wallet(customer.wallet, order)
    order.refresh_from_db()

    # updating order to SHIPPED process
    shipping_data = {
        "tracking_code": 12341234,
    }
    first_variant, second_variant = product.variants.first(), product.variants.last()
    pre_update_reserved_stocks = (
        first_variant.reserved_stock,
        second_variant.reserved_stock,
    )
    pre_update_on_hand_stocks = (
        first_variant.on_hand_stock,
        second_variant.on_hand_stock,
    )
    update_order_to_shipped(order, shipping_data)
    first_variant.refresh_from_db()
    second_variant.refresh_from_db()

    assert order.status == Order.SHIPPED
    assert order.tracking_code == shipping_data["tracking_code"]
    assert pre_update_reserved_stocks == (
        first_variant.reserved_stock + 10,
        second_variant.reserved_stock + 10,
    )
    assert pre_update_on_hand_stocks == (
        first_variant.on_hand_stock + 10,
        second_variant.on_hand_stock + 10,
    )


@pytest.mark.django_db
def test_cancelling_unpaid_order(customer_and_seller, sample_product_instance_factory):
    # prepare the data
    customer, seller = customer_and_seller
    product = sample_product_instance_factory()
    for variant in product.variants.all():
        CartItem.objects.create(
            cart=customer.cart,
            product_variant=variant,
            quantity=10,
        )
    order_creation_data = {
        "user": customer,
        "notes": "ooooo",
        "customer_address": customer.customer_addresses.first(),
    }
    order = process_order_creation(order_creation_data)
    order_cancel_data = {"cancel_reason": "too many orders"}
    first_variant, second_variant = product.variants.first(), product.variants.last()
    pre_update_reserved_stocks = (
        first_variant.reserved_stock,
        second_variant.reserved_stock,
    )
    initial_wallet_balance = customer.wallet.balance
    pay_order_using_wallet(customer.wallet, order)
    refund_transaction = update_order_to_cancelled(order, order_cancel_data)
    first_variant.refresh_from_db()
    second_variant.refresh_from_db()

    assert order.status == Order.CANCELLED
    assert order.cancel_reason
    assert pre_update_reserved_stocks == (
        first_variant.reserved_stock + 10,
        second_variant.reserved_stock + 10,
    )

    # since the payment was completed using wallet, its
    # expected that the paid amount has been refunded to
    # customer's wallet.

    customer.wallet.refresh_from_db()
    assert customer.wallet.balance == initial_wallet_balance
    assert refund_transaction.type == FinancialRecord.WALLET_REFUND
    assert refund_transaction.amount == order.get_total_price()
