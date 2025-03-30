import pytest

from backend.e_commerce.ecom_user_profile.tests.profile_factory import SellerFactory
from product.models import TechnicalDetail
from product.serializers import (
    ProductSellerSerializer,
    ProductSerializerForAny,
    ProductSerializerForOwner,
    ProductVariantSerializerForAny,
    TechnicalDetailSerializer,
)
from product.tests.product_factory import (
    ProductFactory,
    ProductVariantFactory,
    TechnicalDetailFactory,
)

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
    
    serializer = ProductSellerSerializer()

@pytest.mark.django_db
def test_product_serializer_for_any_representation():
    product = ProductFactory()
    technical_details = TechnicalDetailFactory.create_batch(5, product=product)
    variants = ProductVariantFactory.create_batch(5, product=product)

    technical_serializer = TechnicalDetailSerializer(technical_details, many=True)
    variant_serializer = ProductVariantSerializerForAny(variants, many=True)
    product_owner_serializer = ProductSellerSerializer(product.owner.seller_profile)

    product_serializer = ProductSerializerForAny(product)
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
    }
    assert product_serializer.data == expected_data


@pytest.mark.django_db
def test_product_serializer_create(
    sample_product_data_factory,
    subcategory_obj,
    tag_objs,
):
    "Note that technical detail and variant creation/update is not handled in this serializer"
    # create sample data, assign subcategory and tags to it.
    sample_product_data = sample_product_data_factory()
    sample_product_data["subcategory"] = subcategory_obj.id
    sample_product_data["tags"] = [tag.id for tag in tag_objs]

    # initialize and validate the serializer
    serializer = ProductSerializerForOwner(data=sample_product_data)
    serializer.is_valid()
    assert not serializer.errors
    created_product_instance = serializer.save()
    assert list(created_product_instance.tags.all()) == tag_objs
    assert created_product_instance.subcategory == subcategory_obj
    assert created_product_instance.name == sample_product_data["name"]
