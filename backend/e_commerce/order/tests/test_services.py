import pytest
from order.services.management import process_order_creation, pay_order_using_wallet
from order.models import Cart, CartItem, Order
from financeops.models import Transaction

# Note that the input data for the functions in the
# `process_order_creation` module are expected to
# be validated serializer data.


@pytest.mark.django_db
def test_process_order_creation(
    customer_and_seller, sample_product_instance_factory
):
    customer, seller = customer_and_seller()
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
def test_pay_order_using_wallet(
    customer_and_seller, sample_product_instance_factory
):
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

    assert transaction_obj.type == Transaction.WALLET_PAYMENT
    assert transaction_obj.amount == order.get_total_price()
    assert transaction_obj.order == order
