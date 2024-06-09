import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from ecom_user.models import EcomUser

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
def test_user_can_partial_update_customer_profile(api_client_with_credentials):
    url = reverse("customer-profile")
    new_bio = 'Bing chilling with a chocolate ice cream'
    data = {
        'bio': new_bio
    }
    patch_response = api_client_with_credentials.patch(url, data=data)
    assert patch_response.status_code == 200
    # check if the information got updated
    get_repsonse = api_client_with_credentials.get(url)
    assert get_repsonse.status_code == 200
    assert get_repsonse.data['bio'] == new_bio
    
@pytest.mark.django_db
def test_user_is_not_eligible_for_selling(api_client_with_credentials):
    pass