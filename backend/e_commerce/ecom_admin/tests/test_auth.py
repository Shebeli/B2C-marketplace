import pytest

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from ecom_admin.models import EcomAdmin

# ------------
# fixtures
# ------------


@pytest.fixture
def admin_credentials():
    return {"email": "Test123@gmail.com", "username": "TestAdmin", "password": "1234"}


@pytest.fixture
def admin_instance(db, admin_credentials):
    return EcomAdmin.objects.create_user(**admin_credentials)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def refresh_token(admin_instance):
    token = RefreshToken.for_user(admin_instance)
    token['user_type'] = 'admin'
    return token

# -----------
# tests
# -----------


@pytest.mark.django_db
def test_admin_can_obtain_pair_token(api_client, admin_credentials, admin_instance):
    url = reverse("admin-token-obtain-pair")
    response = api_client.post(url, data=admin_credentials)
    assert response.status_code == 200
    assert response.data.get("refresh")
    assert response.data.get("access")


@pytest.mark.django_db
def test_admin_can_verify_token(api_client, refresh_token, admin_instance):
    url = reverse("admin-token-verify")
    response = api_client.post(url, data={"token": str(refresh_token)})
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_can_obtain_access_token(api_client, refresh_token, admin_instance):
    url = reverse("admin-token-refresh")
    response = api_client.post(url, data={"refresh": str(refresh_token)})
    assert response.status_code == 200
    token = AccessToken(response.data["access"]) 
    assert token['user_type'] == 'admin'
    