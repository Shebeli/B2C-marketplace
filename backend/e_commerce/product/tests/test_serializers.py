import pytest

from django.db.models import QuerySet

from product.serializers import ProductSerializerForAny
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
def sample_product_data_factory():
    def create_data():
        return {
            "name": "EO Plastic Chair 2-RS",
            "main_price": 200,
            "description": "A furniture for sitting",
        }

    return create_data


@pytest.fixture
def full_product_data_factory(
    sample_product_data_factory, sample_variants_data, sample_technical_data
):
    def create_full_product_data():
        return {
            "product": dict(sample_product_data_factory()),
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
def subcategory_obj(sample_category_instance_factory):
    return sample_category_instance_factory()["subcategory"]


@pytest.fixture
def sample_tags_instances_factory():
    def create_tags():
        tag_names = ["Chair", "Plastic", "Furniture"]
        tag_objs = []
        for tag_name in tag_names:
            tag_obj = Tag.objects.create(name=tag_name)
            tag_objs.append(tag_obj)
        return tag_objs

    return create_tags


@pytest.fixture
def tag_objs(sample_tags_instances_factory):
    return sample_tags_instances_factory()


@pytest.fixture
def sample_product_instance_factory(
    db,
    full_product_data_factory,
    sample_category_instance_factory,
    sample_tags_instances_factory,
):
    # create the product and the subcategory
    def create_product_instance():
        full_product_data = full_product_data_factory()
        category_objs = sample_category_instance_factory()
        product_obj = Product.objects.create(
            subcategory=category_objs["subcategory_obj"], **full_product_data["product"]
        )
        # create the Tag objects and set the relations
        tag_objs = sample_tags_instances_factory()
        for tag_obj in tag_objs:
            product_obj.tags.add(tag_obj)
        # create variants and TechnicalDetail objects
        for variant in full_product_data["variants"]:
            ProductVariant.objects.create(product=product_obj, **variant)
        for technical in full_product_data["technical"]:
            TechnicalDetail.objects.create(product=product_obj, **technical)
        return product_obj

    return create_product_instance


@pytest.mark.django_db
def test_product_serializer_representation(sample_product_instance_factory):
    # initialize the instance and the serializer
    sample_product_instance = sample_product_instance_factory()
    serializer = ProductSerializerForAny(instance=sample_product_instance)

    # construct technical details representation of the product
    technical_details_repr = []
    for technical_detail in sample_product_instance.technical_details.all():
        technical_details_repr.append(
            {technical_detail.attribute: technical_detail.value}
        )

    # construct product variant representation of the product
    variants_repr = []
    for variant in sample_product_instance.variants.all():
        variants_repr.append(
            {
                "name": variant.name,
                "stock": variant.stock,
                "reserved_stock": variant.reserved_stock,
                "available_stock": variant.available_stock,
                "images": (
                    []
                    if not variant.images
                    else [variant_image.image for variant_image in variant.images.all()]
                ),
                "numbers_sold": variant.numbers_sold,
                "price": variant.price,
            }
        )
    # assertion
    assert serializer.data == {
        "id": 1,
        "technical_details": technical_details_repr,
        "variants": variants_repr,
        "tags": sample_product_instance.tag_names,
        "name": sample_product_instance.name,
        "main_price": sample_product_instance.main_price,
        "main_image": (
            None
            if not (sample_product_instance.main_image)
            else sample_product_instance.main_image
        ),
        "description": sample_product_instance.description,
        "subcategory": sample_product_instance.subcategory.name,
    }


@pytest.mark.django_db
def test_product_serializer_create(
    sample_product_data_factory,
    subcategory_obj,
    tag_objs,
):
    "Note that technical detail and variant creation/update is not handled in this serializer"
    # create sample data, assign subcategory and tags to it.
    sample_product_data = sample_product_data_factory()
    sample_product_data["subcategory"] = subcategory_obj
    sample_product_data["tags"] = [tag.id for tag in tag_objs]

    # initialize the validate the serializer
    serializer = ProductSerializerForAny(data=sample_product_data)
    assert serializer.is_valid()

    created_product_instance = serializer.save()
    assert list(created_product_instance.tags.all()) == tag_objs
    assert created_product_instance.subcategory == subcategory_obj
    assert created_product_instance.name == sample_product_data["name"]
