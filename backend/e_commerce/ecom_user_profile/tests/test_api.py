import pytest
from django.urls import reverse
from ecom_user.models import EcomUser
from rest_framework.test import APIClient

from ecom_user_profile.models import CustomerAddress

# ---------------
#    Fixtures
# ---------------


@pytest.fixture
def user_credentials():
    return {"phone": "09377964142", "password": "1234"}


@pytest.fixture
def user_instance(db, user_credentials):
    return EcomUser.objects.create_user(**user_credentials)


@pytest.fixture
def api_client_with_credentials(db, user_instance):
    api_client = APIClient()
    api_client.force_authenticate(user=user_instance)
    return api_client


# ---------------
#   Test Cases
# ---------------


@pytest.mark.django_db
def test_user_can_retrieve_customer_profile(api_client_with_credentials):
    url = reverse("customer-profile")
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_can_update_customer_profile(api_client_with_credentials):
    url = reverse("customer-profile")
    new_bio = "Bing chilling with a chocolate ice cream"
    data = {"bio": new_bio}
    patch_response = api_client_with_credentials.patch(url, data=data)
    assert patch_response.status_code == 200
    assert patch_response.data["bio"] == new_bio


@pytest.mark.django_db
def test_users_seller_profile_should_be_not_eligible_by_default(
    api_client_with_credentials,
):
    url = reverse("seller-profile")
    response = api_client_with_credentials.get(url)
    assert response.data["is_verified"] == False


@pytest.mark.django_db
def test_user_can_update_seller_profile(api_client_with_credentials):
    url = reverse("seller-profile")
    data = {
        "store_address": "Bleh",
    }
    patch_response = api_client_with_credentials.patch(url, data=data)
    assert patch_response.data["store_address"] == "Bleh"
    put_response = api_client_with_credentials.put(url, data=data)
    assert put_response.data["store_address"] == "Bleh"


@pytest.mark.django_db
def test_user_cannot_create_customer_addresses_more_than_limit(
    api_client_with_credentials, user_instance
):
    for i in range(1, 6):
        CustomerAddress.objects.create(user=user_instance, address=f"address_{i}")
    url = reverse("customer-addresses-list")
    response = api_client_with_credentials.post(url, data={"address": "A new address"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_can_create_list_customer_addresses(api_client_with_credentials):
    url = reverse("customer-addresses-list")
    # user can create multiple addresses
    address_1 = {"address": "AAAA", "postal_code": "1653879533"}
    address_2 = {"address": "OOOO"}
    response_1 = api_client_with_credentials.post(url, data=address_1)
    response_2 = api_client_with_credentials.post(url, data=address_2)
    assert response_1.status_code == 201
    assert response_2.status_code == 201

    # see if the new addresses are listed
    get_response = api_client_with_credentials.get(url)
    assert dict(get_response.data["results"][0])["address"] == address_1["address"]
    assert dict(get_response.data["results"][1])["address"] == address_2["address"]


@pytest.mark.django_db
def test_user_can_destroy_update_retrieve_customer_addresses(
    api_client_with_credentials, user_instance
):
    urls = []
    for i in range(1, 4):
        address_obj = CustomerAddress.objects.create(
            user=user_instance, address=f"address_{i}"
        )
        urls.append(  # ith index of the array 'urls' is mapped to current iteration of CustomerAddress object id
            reverse("customer-addresses-detail", args=[address_obj.id]),
        )

    # deletion
    delete_response = api_client_with_credentials.delete(urls[0])
    assert delete_response.status_code == 204

    # update
    update_response = api_client_with_credentials.patch(
        urls[1], data={"address": "new address"}
    )
    assert update_response.data["address"] == "new address"

    # retrieve
    get_response = api_client_with_credentials.get(urls[2])
    assert get_response.data["address"] == "address_3"
