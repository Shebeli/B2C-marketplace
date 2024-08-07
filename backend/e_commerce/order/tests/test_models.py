import pytest

from order.models import Order, Cart, CartItem, OrderItem


@pytest.mark.django_db
def test_cart_model(sample_product_instance_factory):
    product = sample_product_instance_factory()
    user = product.owner
    cart = Cart.objects.create(user=user)
    assert cart.created_at
    assert cart.updated_at
    assert user.carts.first() == cart


@pytest.mark.django_db
def test_cart_item_model(sample_product_instance_factory):
    product = sample_product_instance_factory()
    user = product.owner
    cart = Cart.objects.create(user=user)
    cart_items = []
    for variant in product.variants.all():
        cart_item = CartItem.objects.create(
            cart=cart, product_variant=variant, quantity=10
        )
        cart_items.append(cart_item)
        assert cart_item.added_at
        assert cart_item.get_total_price() == 10 * variant.price
    assert cart.get_total_price() == sum([cart_item.get_total_price() for cart_item in cart_items])
    
# when an order is attempted to be created, it should be 
# created not by inputs but rather, using the current user's cart items,
# and delete the cart afterwards.
# First, it should be checked for if the customer's account is valid
# (e.g. an already going on order from the same customer shouldn't exist, 
# customer has at least one customer address, 
# the cart items have available stocks for the chosen items  
# which should be immediatly be put into reserved_stock and so on)
# Second, if theres no complaint  from the customer for 3-7 days  
# then the order's status should be changed to COMPLETED 
# (this process should be handled using celery).
# After the order's status is set to COMPLETED, 
# the earned revenue from the order will be deposited into the 
# seller's wallet using the following formula:
# money - (web app % fee).
# The customer is eligible to put reviews for purchased products
# after the order's status is set to DELIVERED.
# @pytest.mark.django_db
# def test_order_model(sample)