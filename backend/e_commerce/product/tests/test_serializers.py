import pytest
from backend.e_commerce.product.serializers.base import ProductListSerializer
from django.core.cache import cache
from django.db.models import Avg, Count
from django.urls import reverse
from ecom_user_profile.tests.profile_factory import SellerFactory
from feedback.tests.feedback_factory import ProductReviewFactory

from product.models import Product
from product.serializers import (
    ProductSellerSerializer,
    ProductSerializerForAny,
    ProductSerializerForOwner,
    ProductVariantSerializerForAny,
    ProductVariantSerializerForOwner,
    TechnicalDetailSerializer,
)
from product.tests.product_factory import (
    ProductFactory,
    ProductVariantFactory,
    SubCategoryBreadCrumbFactory,
    TagFactory,
    TechnicalDetailFactory,
)


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


# ---------------
#   Test cases
# ---------------


@pytest.mark.django_db
def test_product_technical_detail_serializer_repr():
    technical_detail = TechnicalDetailFactory()

    serializer = TechnicalDetailSerializer(technical_detail)
    expected_data = {
        "id": technical_detail.id,
        "attribute": technical_detail.attribute,
        "value": technical_detail.value,
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_product_variant_serializer_any_repr():
    variant = ProductVariantFactory()

    serializer = ProductVariantSerializerForAny(variant)
    expected_data = {
        "id": variant.id,
        "name": variant.name,
        "price": variant.price,
        "images": [variant.image.url for variant in variant.images.all()]
        if variant.images
        else None,
        "color": variant.color,
    }

    assert serializer.data == expected_data


@pytest.mark.django_db
def test_product_seller_serializer_repr():
    seller_user = SellerFactory()
    serializer = ProductSellerSerializer(seller_user)

    expected_data = {
        "id": seller_user.id,
        "store_name": seller_user.seller_profile.store_name,
        "store_image": seller_user.seller_profile.store_image.url
        if seller_user.seller_profile.store_image
        else None,
    }
    assert expected_data == serializer.data


@pytest.mark.django_db
def test_product_serializer_for_any_representation():
    # db objects preparation
    product = ProductFactory()
    technical_details = TechnicalDetailFactory.create_batch(5, product=product)
    variants = ProductVariantFactory.create_batch(5, product=product)
    ProductReviewFactory.create_batch(10, product=product)

    # nested data preperation
    technical_serializer = TechnicalDetailSerializer(technical_details, many=True)
    variant_serializer = ProductVariantSerializerForAny(variants, many=True)
    product_owner_serializer = ProductSellerSerializer(product.owner.seller_profile)

    # serializer preperation
    product_serializer_data = ProductSerializerForAny(product).data
    product_serializer_data["technical_details"].sort(key=lambda x: x["id"])

    # aggregation fields
    rating_avg = product.reviews.aggregate(avg=Avg("rating"))["avg"]
    rating_count = product.reviews.aggregate(count=Count("rating"))["count"]

    expected_data = {
        "id": product.id,
        "owner": product_owner_serializer.data,
        "technical_details": technical_serializer.data,
        "variants": variant_serializer.data,
        "tags": [tag.name for tag in product.tags.all()],
        "name": product.name,
        "is_valid": product.is_valid,
        "description": product.description,
        "subcategory": product.subcategory.name,
        "is_enabled": product.is_enabled,
        "rating_avg": rating_avg,
        "rating_count": rating_count,
    }
    assert product_serializer_data == expected_data
    assert cache.get(f"product:{product.id}:rating_avg") == rating_avg
    assert cache.get(f"product:{product.id}:rating_count") == rating_count


@pytest.mark.django_db
def test_product_serializer_for_owner_represenation():
    # db objects prep
    product: Product = ProductFactory()
    technical_details = TechnicalDetailFactory.create_batch(5, product=product)
    variants = ProductVariantFactory.create_batch(5, product=product)
    ProductReviewFactory.create_batch(10, product=product)

    # nested data prep
    technical_serializer = TechnicalDetailSerializer(technical_details, many=True)
    variant_serializer = ProductVariantSerializerForOwner(variants, many=True)

    # serializer prep
    product_serializer_data = ProductSerializerForOwner(product).data
    product_serializer_data["technical_details"].sort(key=lambda x: x["id"])
    product_serializer_data["variants"].sort(key=lambda x: x["id"])

    # aggregation fields prep
    rating_avg = product.get_rating_avg()
    rating_count = product.get_rating_count()
    total_revenue = product.get_total_revenue()
    total_orders = product.get_total_orders()
    total_units_sold = product.get_total_units_sold()

    expected_data = {
        "id": product.id,
        "name": product.name,
        "created_at": product_serializer_data["created_at"],
        "description": product.description,
        "main_variant": product.main_variant.id,
        "main_price": product.main_variant.price,
        "main_image": product.main_variant.image.url
        if product.main_variant.image
        else None,
        "technical_details": technical_serializer.data,
        "subcategory": {"id": product.subcategory.id, "name": product.subcategory.name},
        "tags": [tag.name for tag in product.tags.all()],
        "variants": variant_serializer.data,
        "on_hand_stock": product.get_on_hand_stock(),
        "reserved_stock": product.get_reserved_stock(),
        "available_stock": product.get_available_stock(),
        "view_count": product.view_count,
        "number_sold": product.get_number_sold(),
        "is_valid": product.is_valid,
        "is_enabled": product.is_enabled,
        "rating_avg": rating_avg,
        "rating_count": rating_count,
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_units_sold": total_units_sold,
    }
    assert expected_data == product_serializer_data

    # its expected that the serializer has cached aggregation/calculation fields
    assert cache.get(f"product:{product.id}:rating_avg") == rating_avg
    assert cache.get(f"product:{product.id}:rating_count") == rating_count
    assert cache.get(f"product:{product.id}:total_revenue") == total_revenue
    assert cache.get(f"product:{product.id}:total_orders") == total_orders
    assert cache.get(f"product:{product.id}:total_units_sold") == total_units_sold


@pytest.mark.django_db
def test_product_serializer_create():
    "Note that technical detail and variant creation/update is not handled in this serializer"
    # prep the data
    owner = SellerFactory()
    subcategory = SubCategoryBreadCrumbFactory()
    tags = TagFactory.create_batch(5)
    product_data = {
        "owner": owner.id,
        "name": "A new product",
        "description": "A new description for new product",
        "subcategory": subcategory.id,
        "tags": [tag.id for tag in tags],
    }

    # initialize and validate the serializer
    serializer = ProductSerializerForOwner(data=product_data)
    assert serializer.is_valid(), f"Serializer errors :{serializer.errors}"

    product = serializer.save()
    expected_data = {
        "owner": owner.id,
        "name": product.name,
        "description": product.description,
        "subcategory": product.subcategory.id,
        "tags": [tag.id for tag in product.tags.all()],
    }

    assert expected_data == product_data


@pytest.mark.django_db
def test_product_list_represenation():
    products = ProductFactory.create_batch(10)
    for product in products:
        ProductVariantFactory(product=product)

    serializer = ProductListSerializer(products, many=True)
    expected_data = [
        {
            "id": product.id,
            "name": product.name,
            "main_price": product.main_variant.price,
            "main_image": product.main_variant.image.url
            if product.main_variant.image
            else None,
            "seller_profile": {
                "store_name": product.owner.seller_profile.store_name,
                "store_image": product.owner.seller_profile.store_image.url
                if product.owner.seller_profile.store_image
                else None,
                "store_url": reverse(
                    "seller-public-profile",
                    kwargs={"pk": product.owner.seller_profile.id},
                ),
            },
        }
        for product in products
    ]
    assert serializer.data == expected_data
