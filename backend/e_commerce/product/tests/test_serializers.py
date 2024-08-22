import pytest

from product.serializers import ProductSerializerForAny, ProductSerializerForOwner

# ---------------
#   Test cases
# ---------------


@pytest.mark.django_db
def test_product_serializer_for_any_representation(sample_product_instance_factory):
    # initialize the instance and the serializer
    sample_product_instance = sample_product_instance_factory()
    serializer = ProductSerializerForAny(instance=sample_product_instance)

    # construct technical details representation of the product
    technical_details_repr = []
    for technical_detail in sample_product_instance.technical_details.all():
        technical_details_repr.append(
            {
                "id": technical_detail.id,
                "attribute": technical_detail.attribute,
                "value": technical_detail.value,
            }
        )

    # construct product variant representation of the product
    variants_repr = []
    for variant in sample_product_instance.variants.all():
        variants_repr.append(
            {
                "id": variant.id,
                "name": variant.name,
                "images": (
                    []
                    if not variant.images
                    else [variant_image.image for variant_image in variant.images.all()]
                ),
                "price": variant.price,
            }
        )
    assert serializer.data == {
        "id": sample_product_instance.id,
        "owner": (
            sample_product_instance.owner.id if sample_product_instance.owner else None
        ),
        "technical_details": technical_details_repr,
        "variants": variants_repr,
        "tags": sample_product_instance.tag_names,
        "name": sample_product_instance.name,
        "rating": str(sample_product_instance.rating),
        "is_valid": sample_product_instance.is_valid,
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
