import pytest

from product.serializers import ProductSerializer
from product.models import (
    Product,
    TechnicalDetail,
    ProductVariant,
    Tag,
    SubCategory,
    Category,
    MainCategory,
)


@pytest.fixture
def sample_variants_data():
    return [
        {"name": "blue", "price": 195, "stock": 15},
        {"name": "white", "price": 200, "stock": 50},
    ]


@pytest.fixture
def sample_technical_data():
    return [
        {"attribute": "Material", "value": "Plastic"},
        {"attribute": "weight", "value": "300 grams"},
    ]


@pytest.fixture
def sample_product_data():
    return {
        "name": "EO Plastic Chair 2-RS",
        "main_price": 200,
        "description": "A furniture for sitting",
        "tag_names": ["chair", "plastic", "furniture"],
    }


@pytest.fixture
def full_product_data_factory(
    sample_product_data, sample_variants_data, sample_technical_data
):
    def create_full_product_data():
        return {
            "product": dict(sample_product_data),
            "variants": list(sample_variants_data),
            "technical": list(sample_technical_data),
        }

    return create_full_product_data


@pytest.fixture
def sample_category_instance_factory():
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
def sample_product_instance(
    db, full_product_data_factory, sample_category_instance_factory
):
    full_product_data = full_product_data_factory()
    tag_names = full_product_data["product"].pop("tag_names")
    # create the categories and the product
    category_objs = sample_category_instance_factory()
    product_obj = Product.objects.create(
        subcategory=category_objs["subcategory_obj"], **full_product_data["product"]
    )
    # create the Tag objects and set the relations
    for tag_name in tag_names:
        tag_obj = Tag.objects.create(name=tag_name)
        product_obj.tags.add(tag_obj)
    # create variants and TechnicalDetail objects
    for variant in full_product_data["variants"]:
        ProductVariant.objects.create(product=product_obj, **variant)
    for technical in full_product_data["technical"]:
        TechnicalDetail.objects.create(product=product_obj, **technical)
    return product_obj


@pytest.mark.django_db
def test_product_correct_representation(sample_product_instance):
    serializer = ProductSerializer(instance=sample_product_instance)
    technical_details_repr = []
    for technical_detail in sample_product_instance.technical_details:
        technical_details_repr.append(
            {technical_detail.attribute: technical_detail.value}
        )
    variants_repr = []
    for variant in sample_product_instance.variants:
        variants_repr.append(
            {
                "variation_name": variant.variation_name,
                "stock": variant.stock,
                "reserved_stock": variant.reserved_stock,
                "available_stock": variant.available_stock,
                "images": variant.images,
                "numbers_sold": variant.numbers_sold,
                "price": variant.price,
            }
        )
    assert serializer.data == {
        "id": 1,
        "technical_details": technical_details_repr,
        "variants": variants_repr,
        "tags": sample_product_instance.tag_names,
        "name": sample_product_instance.name,
        "main_price": sample_product_instance.price,
        "description": sample_product_instance.description,
        "subcategory": sample_product_instance.subcategory.name,
    }
