import pytest
from django.core.cache import cache
from django.urls import reverse
from ecom_user.models import EcomUser
from rest_framework.test import APIClient

from product.models import Product, ProductVariant, TechnicalDetail

# ---------------
#    Fixtures
# ---------------


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def customer_credentials():
    return {"phone": "09377964142", "password": "1234"}


@pytest.fixture
def seller_credentials():
    return {"phone": "09377964143", "password": "1234"}


@pytest.fixture
def customer_instance(db, customer_credentials):
    return EcomUser.objects.create_user(**customer_credentials)


@pytest.fixture
def seller_instance(db, seller_credentials):
    user = EcomUser.objects.create_user(**seller_credentials)
    user.seller_profile.is_verified = True
    user.save()
    return user


@pytest.fixture
def product_instance_factory(sample_product_instance_factory, seller_instance):
    def create_product():
        product = sample_product_instance_factory()
        product.owner = seller_instance
        product.save()
        return product

    return create_product


@pytest.fixture
def api_client_with_customer_credentials(db, customer_instance):
    api_client = APIClient()
    api_client.force_authenticate(user=customer_instance)
    return api_client


@pytest.fixture
def api_client_with_seller_credentials(db, seller_instance):
    api_client = APIClient()
    api_client.force_authenticate(user=seller_instance)
    return api_client


# ---------------
#   Test Cases
# ---------------


@pytest.mark.django_db
def test_seller_can_create_product(
    api_client_with_seller_credentials, sample_product_data_factory
):
    url = reverse("product-list")
    product_data = sample_product_data_factory()
    response = api_client_with_seller_credentials.post(url, data=product_data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_seller_can_delete_owned_product(
    api_client_with_seller_credentials, product_instance_factory
):
    product = product_instance_factory()
    url = reverse("product-detail", args=[product.id])
    response = api_client_with_seller_credentials.delete(url, data={"id": product.id})
    assert response.status_code == 204


@pytest.mark.django_db
def test_seller_can_update_owned_product(
    api_client_with_seller_credentials, product_instance_factory
):
    product = product_instance_factory()
    url = reverse("product-detail", args=[product.id])
    response = api_client_with_seller_credentials.patch(url, data={"name": "new name"})
    assert response.status_code == 200
    assert response.data["name"] == "new name"


@pytest.mark.django_db
def test_product_view_count_increases_on_view(
    api_client_with_seller_credentials, product_instance_factory
):
    client_ip = "127.0.0.1"  # default ip used by APIClient
    redis_client = cache.client.get_client()
    product = product_instance_factory()
    url = reverse("product-detail", args=[product.id])
    response = api_client_with_seller_credentials.get(url)
    assert response.status_code == 200

    # check to see if the cache key has been created for tracking
    redis_key = f"product:{product.id}:ip:{client_ip}"
    assert redis_client.exists(redis_key) == 1

    # check to see if the view count has increased
    product = Product.objects.get(id=product.id)
    assert product.view_count == 1


@pytest.mark.django_db
def test_product_can_be_created(
    api_client_with_seller_credentials, tag_objs, subcategory_obj
):
    url = reverse("product-list")
    response = api_client_with_seller_credentials.post(
        url,
        data={
            "name": "chair",
            "subcategory": subcategory_obj.id,
            "tags": [tag.id for tag in tag_objs],
        },
    )
    print(response.data)
    assert response.status_code == 201
    assert Product.objects.get(id=response.data["id"])


@pytest.mark.django_db
def test_product_has_extra_details_for_owner(
    api_client_with_seller_credentials, product_instance_factory
):
    product = product_instance_factory()
    url = reverse("product-detail", args=[product.id])
    response = api_client_with_seller_credentials.get(url)
    product.refresh_from_db(fields=["view_count"])
    assert response.data.get("view_count") == product.view_count
    assert response.data.get("number_sold") == product.get_number_sold()
    assert response.data.get("available_stock") == product.get_available_stock()


@pytest.mark.django_db
def test_product_variant_retrieve_update_destroy(
    api_client_with_seller_credentials, product_instance_factory
):
    product = product_instance_factory()
    variant = ProductVariant.objects.create(
        product=product, name="some variant", price=200, on_hand_stock=20
    )
    url = reverse(
        "variant-detail",
        args=[product.id, variant.id],
    )

    # retrieve
    get_response = api_client_with_seller_credentials.get(url)
    assert get_response.status_code == 200
    assert get_response.data["id"] == variant.id
    assert get_response.data["name"] == variant.name
    assert get_response.data["on_hand_stock"] == variant.on_hand_stock

    # update
    update_data = {"name": "new variant name", "price": 205}
    put_response = api_client_with_seller_credentials.patch(url, data=update_data)
    assert put_response.status_code == 200
    assert put_response.data["name"] == update_data["name"]
    assert put_response.data["price"] == update_data["price"]

    # destroy
    delete_response = api_client_with_seller_credentials.delete(url)
    assert delete_response.status_code == 204


@pytest.mark.django_db
def test_product_variant_list_create(
    api_client_with_seller_credentials, product_instance_factory
):
    product_instance = product_instance_factory()
    url = reverse("variant-list", args=[product_instance.id])
    variants = []
    for i in range(3):
        variant = ProductVariant.objects.create(
            product=product_instance,
            name=f"Product variant {i}",
            price=100 * i,
            on_hand_stock=20,
        )
        variants.append(variant)

    # create
    post_data = {"name": "New variant", "price": 250, "on_hand_stock": 50}
    post_response = api_client_with_seller_credentials.post(url, data=post_data)
    assert post_response.status_code == 201
    assert post_response.data["name"] == post_data["name"]
    assert post_response.data["price"] == post_data["price"]

    # list
    get_response = api_client_with_seller_credentials.get(url)
    variants = ProductVariant.objects.filter(product=product_instance)
    assert get_response.status_code == 200
    for i in range(len(variants)):  # len(variants) = len(get_response.data)
        assert variants[i].id == get_response.data["results"][i]["id"]
        assert variants[i].name == get_response.data["results"][i]["name"]
        assert variants[i].price == get_response.data["results"][i]["price"]


@pytest.mark.django_db
def test_product_technical_retrieve_update_destroy(
    api_client_with_seller_credentials, product_instance_factory
):
    product = product_instance_factory()
    technical_detail = TechnicalDetail.objects.create(
        product=product, attribute="some attribute", value="some value"
    )
    url = reverse(
        "technical-info-detail",
        args=[product.id, technical_detail.id],
    )

    # retrieve
    get_response = api_client_with_seller_credentials.get(url)
    assert get_response.status_code == 200
    assert {get_response.data["attribute"]: get_response.data["value"]} == {
        technical_detail.attribute: technical_detail.value
    }

    # update
    update_data = {"attribute": "new attribute", "value": "new value"}
    put_response = api_client_with_seller_credentials.patch(url, data=update_data)
    assert put_response.status_code == 200
    assert {put_response.data["attribute"]: put_response.data["value"]} == {
        update_data["attribute"]: update_data["value"]
    }

    # destroy
    delete_response = api_client_with_seller_credentials.delete(url)
    assert delete_response.status_code == 204


def test_technical_list_create(
    api_client_with_seller_credentials, product_instance_factory
):
    # initialize the product and sample technical details
    product_instance = product_instance_factory()
    url = reverse("technical-info-list", args=[product_instance.id])
    technicals = []
    for i in range(1, 4):
        technical = TechnicalDetail.objects.create(
            product=product_instance, attribute=f"attribute {i}", value=f"value {i}"
        )
        technicals.append(technical)

    # single object creation
    post_data = {"attribute": "material", "value": "plastic"}
    post_response = api_client_with_seller_credentials.post(url, data=post_data)
    assert post_response.status_code == 201
    assert post_response.data["attribute"] == post_data["attribute"]
    assert post_response.data["value"] == post_data["value"]

    # bulk object creation
    bulk_post_data = [
        {"attribute": "eewraqweq", "value": "250gr"},
        {"attribute": "size", "value": "25cmx50cmx90cm"},
    ]
    bulk_post_response = api_client_with_seller_credentials.post(
        url, data=bulk_post_data, format="json"
    )
    assert bulk_post_response.status_code == 201
    assert {
        bulk_post_response.data[0]["attribute"]: bulk_post_response.data[0]["value"]
    } == {bulk_post_data[0]["attribute"]: bulk_post_data[0]["value"]}

    # list
    get_response = api_client_with_seller_credentials.get(url)
    techincal_details = TechnicalDetail.objects.filter(product=product_instance)
    assert get_response.status_code == 200
    for i in range(len(techincal_details)):  # len(variants) = len(get_response.data)
        response_attribute = get_response.data["results"][i]["attribute"]
        response_value = get_response.data["results"][i]["value"]
        obj_attribute = techincal_details[i].attribute
        obj_value = techincal_details[i].value
        assert {obj_attribute: obj_value} == {response_attribute: response_value}
