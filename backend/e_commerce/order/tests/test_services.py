import pytest
from order.services.management import process_order_creation
from order.models import Cart, CartItem, Order


@pytest.mark.django_db
def test_process_order_creation(customer_and_seller_factory, sample_product_instance_factory):
    customer, _ = customer_and_seller_factory
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
    assert order.customer_notes == data['notes']
    assert order.get_total_price() == cart_total_price
    
    # check the updated stocks
    variant_1 = product.variants.first()
    variant_2 = product.variants.last()
    assert variant_1.reserved_stock == 10
    assert variant_2.reserved_stock == 10
    
    