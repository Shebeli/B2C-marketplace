import pytest

from product.models import Product, ProductVariant, MainCategory, Category, SubCategory
from .test_api import EcomUser


@pytest.fixture
def sample_category_instance_factory(db):
    def create_categories():
        maincategory_obj = MainCategory.objects.create(name="Home and Kitchen")
        category_obj = Category.objects.create(
            name="Couches and Home Decoration", main_category=maincategory_obj
        )
        subcategory_obj = SubCategory.objects.create(
            name="Chair", category=category_obj
        )
        return {
            "maincategory_obj": maincategory_obj,
            "category_obj": category_obj,
            "subcategory_obj": subcategory_obj,
        }

    return create_categories


@pytest.fixture
def product_factory(sample_category_instance_factory):
    def create_product():
        subcategory = sample_category_instance_factory()["subcategory_obj"]
        user = EcomUser.objects.create_user(phone="09377964142")
        product = Product.objects.create(
            owner=user,
            name="Product 1",
            subcategory=subcategory,
        )
        return product

    return create_product


@pytest.mark.django_db
def test_main_variant_assign_on_creation(product_factory):
    product = product_factory()
    assert not product.is_valid
    # test signal assigns the new created variant to product
    variant = ProductVariant.objects.create(
        product=product, price=200, name="variant 1", on_hand_stock=50
    )
    product.refresh_from_db()
    assert product.main_variant == variant
    assert product.is_valid


@pytest.mark.django_db
def test_main_variant_assign_on_delete(product_factory):
    product = product_factory()
    variant_1 = ProductVariant.objects.create(
        product=product, price=250, name="variant 1", on_hand_stock=50
    )
    variant_2 = ProductVariant.objects.create(
        product=product, price=200, name="variant 2", on_hand_stock=40
    )
    product = Product.objects.get(id=product.id)
    assert product.main_variant == variant_1
    # see if the first variant is assigned as main variant after deletion of main variant
    variant_1.delete()
    product = Product.objects.get(id=product.id)
    assert product.main_variant == variant_2
    # main variant should be set to null if no variant remains anymore
    variant_2.delete()
    product = Product.objects.get(id=product.id)
    assert not product.main_variant