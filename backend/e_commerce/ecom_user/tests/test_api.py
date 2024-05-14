import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from ecom_user.utils import create_sms_cooldown_cache_key, create_phone_verify_cache_key

@pytest.fixture
def user_password():
    return "$tR0nG165P@sSwe;oRd09_"

@pytest.fixture
def cache():
    from django.core.cache import cache
    yield cache
    cache.clear()

@pytest.fixture
def generate_user(db, django_user_model, user_password):
    def make_user(**kwargs):
        if not kwargs["phone"]:
            kwargs["phone"] = "09377964148"
        if not kwargs["username"]:
            kwargs["username"] = "some_test_username"
        kwargs["password"] = user_password
        return django_user_model.objects.create_user(**kwargs)
    return make_user

# signup process

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, generate_user, api_client):
    user = generate_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.mark.django_db
def test_user_valid_register_request(api_client):
    url = reverse("user-signup-request-register")
    data = {"phone": "09377964148"}
    response = api_client.post(url, data=data)
    assert response.status_code == 202


@pytest.mark.django_db
def test_user_too_many_register_requests(api_client):
    url = reverse("user-signup-request-register")
    data = {"phone": "09377964148"}
    api_client.post(url, data=data)
    response = api_client.post(url, data=data)
    assert response.status_code == 429

# user verifying their register

@pytest.fixture
def register_verification_code(db, api_client, cache):
    url = reverse("user-signup-request-register")
    data = {"phone": "09377964148"}
    api_client.post(url, data=data)
    return cache.get(create_phone_verify_cache_key(data['phone']))


@pytest.mark.django_db
def test_user_verifies_register(api_client, register_verification_code):
    url = reverse("user-signup-verify-register")
    print(f"\n url: {url}")
    data = {"phone": "09377964148", "code": register_verification_code}
    response = api_client.post(url, data=data)
    assert response.status_code == 201
    assert isinstance(response.data["access"], str)
    assert isinstance(response.data["refresh"], str)
