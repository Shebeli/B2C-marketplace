import pytest

from order.models import Order, Cart, CartItem, OrderItem


@pytest.mark.django_db
def test_cart_model_on_user_creation(customer_instance_factory):
    customer = customer_instance_factory()
    cart = Cart.objects.get(user=customer)
    assert cart


@pytest.mark.django_db
def test_cart_item_model(sample_product_instance_factory):
    product = sample_product_instance_factory()
    user = product.owner
    cart = Cart.objects.get(user=user)
    cart_items = []
    for variant in product.variants.all():
        cart_item = CartItem.objects.create(
            cart=cart, product_variant=variant, quantity=10
        )
        cart_items.append(cart_item)
        assert cart_item.added_at
        assert cart_item.get_total_price() == 10 * variant.price
    assert cart.get_total_price() == sum(
        [cart_item.get_total_price() for cart_item in cart_items]
    )


@pytest.mark.django_db
def test_order_model(sample_product_instance_factory, customer_instance_factory):
    product = sample_product_instance_factory()
    # create order items and the order
    customer = customer_instance_factory()
    order = Order.objects.create(customer=customer, seller=product.owner)
    order_total_price = 0
    for variant in product.variants.all():
        order_item = OrderItem.objects.create(
            order=order,
            product_variant=variant,
            submitted_price=variant.price,
            quantity=5,
        )
        order_total_price += order_item.submitted_price * order_item.quantity
    order.refresh_from_db()
    assert order.get_total_price() == order_total_price
    assert order.seller == product.owner
