import pytest
from order.services.management import process_order_creation
from order.models import Cart, CartItem, Order


@pytest.mark.django_db
def test_process_order_creation(customer_and_seller, sample_product_instance_factory):
    customer, _ = customer_and_seller
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
        "customer_address": customer.address,
    }
    order = process_order_creation(data)
    product.refresh_from_db()
    # check the order and the cart
    assert customer.cart.items.all() == []
    assert order.status == Order.UNPAID
    assert order.customer_address == customer.address
    assert order.notes == data['notes']
    
    # check the updated stocks
    variant_1 = product.variants.first()
    variant_2 = product.variants.last()
    assert variant_1.on_hand_stock == 5 
    assert variant_2.on_hand_stock == 40
    assert variant_1.reserved_stock == 10
    assert variant_2.reserved_stock == 10
    
    