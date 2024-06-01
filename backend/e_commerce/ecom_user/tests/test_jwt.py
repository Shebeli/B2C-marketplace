import pytest

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from ecom_user.models import EcomUser

# ------------
# fixtures
# ------------


@pytest.fixture
def user_credentials():
    return {"phone": "09377964142", "password": "1234"}


@pytest.fixture
def user_instance(db, user_credentials):
    return EcomUser.objects.create_user(**user_credentials)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def refresh_token(user_instance):
    token = RefreshToken.for_user(user_instance)
    token["user_type"] = "normal"
    return token


# -----------
# tests
# -----------


@pytest.mark.django_db
def test_user_can_obtain_pair_token(api_client, user_credentials, user_instance):
    url = reverse("user-token-obtain-pair")
    response = api_client.post(url, data=user_credentials)
    assert response.status_code == 200
    assert response.data.get("refresh")
    assert response.data.get("access")


@pytest.mark.django_db
def test_user_can_verify_token(api_client, refresh_token, user_instance):
    url = reverse("user-token-verify")
    response = api_client.post(url, data={"token": str(refresh_token)})
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_can_obtain_access_token(api_client, refresh_token, user_instance):
    url = reverse("user-token-refresh")
    response = api_client.post(url, data={"refresh": str(refresh_token)})
    assert response.status_code == 200
    token = AccessToken(response.data["access"])
    assert token['user_type'] == 'normal'
