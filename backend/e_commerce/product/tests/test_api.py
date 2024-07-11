import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from ecom_user.models import EcomUser
from ecom_user_profile.models import CustomerAddress
from product.models import Product

# ---------------
#    Fixtures
# ---------------


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
    return EcomUser.objects.create_user(**seller_credentials)


@pytest.fixture
def api_client_with_customer_credentials(db, customer_instance):
    api_client = APIClient()
    api_client.force_authenticate(user=customer_instance)
    return api_client


@pytest.fixture
def api_client_with_seller_credentials(db, customer_instance):
    api_client = APIClient()
    api_client.force_authenticate(user=customer_instance)
    return api_client


# ---------------
#   Test Cases
# ---------------


@pytest.mark.django_db
def test_seller_can_create_product(api_client_with_seller_credentials):
    url = reverse("product-list")
    response = api_client_with_seller_credentials.post(url, data={})
    assert response.status_code == 201


@pytest.mark.django_db
def test_seller_can_delete_owned_product(
    api_client_with_seller_credentials, seller_instance
):
    product = Product.objects.create(owner=seller_instance, name="sample")
    url = reverse("product-detail", args=[product.id])
    response = api_client_with_seller_credentials.delete(url, data={"id": product.id})
    assert response.status_code == 200


@pytest.mark.django_db
def test_seller_can_update_owned_product(
    api_client_with_seller_credentials, seller_instance
):
    product = Product.objects.create(owner=seller_instance, name="sample")
    url = reverse("product-detail", args=[product.id])
    response = api_client_with_seller_credentials.patch(url, data={"name": "new name"})
    assert response.status_code == 200
    assert response.data["name"] == "new name"
