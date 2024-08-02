import random

import pytest


from django.urls import reverse
from rest_framework.test import APIClient

from ecom_user.models import EcomUser
from product.models import (
    SubCategory,
    Category,
    MainCategory,
    Product,
    ProductVariant,
    Tag,
)


# Generate different and considerable numbers of categories for various product
# filter & sort testing.
# For the following fixture, the aim is to create 3 'MainCategory' instances,
# 1 'Category' instance for each created 'MainCategory' instance,
# and 1 'SubCategory' instance for each created 'Category' instance.


@pytest.fixture
def category_instances_factory():
    def create_category_instances():
        main_categories = []
        categories = []
        sub_categories = []
        for i in range(3):
            # main categories
            main_category = MainCategory.objects.create(name=f"MainCategory {i+1}")
            main_categories.append(main_category)

            # categories
            category = Category.objects.create(
                name=f"Category {i+1}", main_category=main_category
            )
            categories.append(category)

            # sub categories
            sub_category = SubCategory.objects.create(
                name=f"SubCategory {i+1}", category=category
            )
            sub_categories.append(sub_category)
        return {
            "main_categories": main_categories,
            "categories": categories,
            "sub_categories": sub_categories,
        }

    return create_category_instances


@pytest.fixture
def tag_instances_factory():
    def create_tags(number_of_tags: int = 3):
        return [Tag.objects.create(name=f"Tag {i+1}") for i in range(number_of_tags)]

    return create_tags


@pytest.fixture
def products_by_subcategories_factory(
    category_instances_factory, tag_instances_factory
):
    def create_products(products_per_subcategory: int = 5):
        categories = category_instances_factory()
        tags = tag_instances_factory()
        subcategories = categories["sub_categories"]
        subcategory_products = {}

        user = EcomUser.objects.create_user(phone="09377964142")
        for i, subcategory in enumerate(subcategories):
            products = []
            for j in range(products_per_subcategory):
                product = Product.objects.create(
                    owner=user,  # to keep the product 'valid'
                    name=f"Product {j}",
                    subcategory=subcategory,
                )
                ProductVariant.objects.create(
                    product=product,
                    price=100 * (i + j + 1),
                    name=f"Product variant {j}",
                    on_hand_stock=random.randint(1, 30) * j,  # 0 for j=0
                )
                product.tags.add(tags[i])
                products.append(product)
            subcategory_products[subcategory.name] = products
        return subcategory_products

    return create_products


# A total of 3 subcategories, with each subcategory having 5 products, prices:
# 100, 200, 300, 400, 500
# 200, 300, 400, 500, 600
# 300, 400, 500, 600, 700


@pytest.mark.django_db
@pytest.mark.parametrize(
    "request_data,expected_len",
    [
        ({"price_min": "200", "price_max": "400"}, 8),
        ({"in_stock": True}, 12),
        ({"name": "Product 1"}, 3),
    ],
)
def test_product_filter(request_data, expected_len, products_by_subcategories_factory):
    api_client = APIClient()
    subcategories_products = products_by_subcategories_factory()
    url = reverse("product-list")
    filtered_products = []
    for subcategory in subcategories_products.keys():
        request_data["subcategory"] = subcategory
        response = api_client.get(url, data=request_data)
        assert response.status_code == 200
        for product in response.data["results"]:
            filtered_products.append(product)
    assert len(filtered_products) == expected_len


@pytest.mark.django_db
def test_product_filter_tags(products_by_subcategories_factory):
    api_client = APIClient()
    subcategories_products = products_by_subcategories_factory()
    url = reverse("product-list")
    filtered_products = []
    for subcategory in subcategories_products.keys():
        request_data = {"tags": [Tag.objects.all()[0].id, Tag.objects.all()[1].id]}
        request_data["subcategory"] = subcategory
        response = api_client.get(url, data=request_data)
        assert response.status_code == 200
        for product in response.data["results"]:
            filtered_products.append(product)
    first_tag_products_count = Tag.objects.all()[0].products.count()
    second_tag_products_count = Tag.objects.all()[1].products.count()
    expected_len = first_tag_products_count + second_tag_products_count
    assert len(filtered_products) == expected_len
