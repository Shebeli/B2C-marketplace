import pytest

from product.models import (
    Category,
    MainCategory,
    Product,
    ProductVariant,
    SubCategory,
    Tag,
    TechnicalDetail,
)


@pytest.fixture
def sample_variants_data():
    return [
        {"name": "blue", "price": 195, "on_hand_stock": 15},
        {"name": "white", "price": 200, "on_hand_stock": 50},
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
def subcategory_obj(sample_category_instance_factory):
    return sample_category_instance_factory()["subcategory_obj"]


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
    def create_product_instance():
        full_product_data = full_product_data_factory()

        # create the subcategory and the product
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
