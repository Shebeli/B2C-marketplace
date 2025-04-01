import pytest

from product.models import Product, ProductVariant, SubCategory


@pytest.mark.django_db
def test_product_queryset_available_stock(sample_product_instance_factory):
    sample_product_instance_factory()
    products = (
        Product.objects.all().with_available_stock()
    )  # variant 1 on-hand stock: 50,variant 2 on-hand stock: 15
    assert products[0].available_stock == 65


@pytest.mark.django_db
def test_product_queryset_number_sold(sample_product_instance_factory):
    sample_product_instance_factory()
    products = Product.objects.all().with_total_number_sold()
    assert products[0].total_number_sold == 0


@pytest.mark.django_db
def test_product_queryset_main_variant_info(sample_product_instance_factory):
    """
    Assuming the signals for assigning main variant object for product instance
    upon object creation of product variant instance is functional.
    """
    sample_product_instance_factory()
    products = Product.objects.all().with_main_variant_info()
    assert products[0].main_price == 195


@pytest.mark.django_db
def test_product_queryset_in_stock(sample_product_instance_factory):
    sample_product_instance_factory()
    products = Product.objects.all()
    products = products.with_in_stock()
    assert products[0].in_stock


@pytest.mark.django_db
def test_product_manager_available(sample_product_instance_factory):
    sample_product_instance_factory()
    products = Product.objects.available()
    assert products[0]


@pytest.mark.django_db
def test_product_manager_unavailable(sample_product_instance_factory):
    sample_product_instance_factory()
    subcategory = SubCategory.objects.first()
    unavailable_product = Product.objects.create(
        name="Unavailable product", subcategory=subcategory
    )
    ProductVariant.objects.create(
        product=unavailable_product, name="SomeVariant", price=500, on_hand_stock=0
    )
    products = Product.objects.unavailable()
    assert products[0] == unavailable_product
