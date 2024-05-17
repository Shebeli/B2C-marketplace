import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from ecom_user.utils import create_sms_cooldown_cache_key, create_phone_verify_cache_key

# USER_SIGNUP_BASENAME = 'user-signup'
# USER_PROFILE_BASENAME = 'user-profile'
# USER_ONETIME_AUTH_BASENAME = 'user-onetime-auth'


@pytest.fixture
def user_password():
    return "$tR0nG165P@sSwe;oRd09_"

@pytest.fixture
def user_data():
    return {"phone": "09377964142"}

@pytest.fixture
def cache():
    from django.core.cache import cache
    yield cache
    cache.clear()

@pytest.fixture
def generate_user(db, django_user_model, user_password):
    def make_user(**kwargs):
        if not kwargs["phone"]:
            kwargs["phone"] = "09377964142"
        if not kwargs["username"]:
            kwargs["username"] = "some_test_username"
        kwargs["password"] = user_password
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, generate_user, api_client):
    user = generate_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)

# UserSignUpViewSet router actions:

# request_register: 

@pytest.mark.django_db
def test_user_valid_register_request(api_client, user_data):
    url = reverse("user-signup-request-registration")
    response = api_client.post(url, data=user_data)
    assert response.status_code == 202


@pytest.mark.django_db
def test_user_too_many_register_requests(api_client, user_data):
    url = reverse("user-signup-request-registration")
    api_client.post(url, data=user_data)
    response = api_client.post(url, data=user_data)
    assert response.status_code == 429

# verify_register: 

@pytest.fixture
def register_verification_code(db, api_client, cache, user_data):
    url = reverse("user-signup-request-registration")
    api_client.post(url, data=user_data)
    return cache.get(create_phone_verify_cache_key(user_data['phone']))


@pytest.mark.django_db
def test_correct_code_for_verifying_register(api_client, register_verification_code, user_data):
    url = reverse("user-signup-verify-registration-request")
    user_data['code'] = register_verification_code
    response = api_client.post(url, data=user_data)
    assert response.status_code == 201
    assert isinstance(response.data["access"], str)
    assert isinstance(response.data["refresh"], str)

@pytest.mark.django_db
def test_incorrect_code_for_verifying_register(api_client, register_verification_code, user_data):
    url = reverse("user-signup-verify-registration-request")
    user_data['code'] = '12345'
    response = api_client.post(url, data=user_data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_unexpected_code_for_verifying_register(api_client, user_data):
    url = reverse("user-signup-verify-registration-request")
    user_data['code'] = '12345'
    response = api_client.post(url, data=user_data)
    assert response.status_code == 400

# UserForgotPasswordViewSet 

# request_onetime_auth

@pytest.mark.django_db
def test_user_valid_request_onetime_auth(api_client, user_data):
    url = reverse("user-onetime-auth-request-auth")
    response = api_client.post(url, data=user_data)
    assert response.status_code == 202


@pytest.mark.django_db
def test_user_too_many_onetime_auth_requests(api_client, user_data):
    url = reverse("user-onetime-auth-request-auth")
    api_client.post(url, data=user_data)
    response = api_client.post(url, data=user_data)
    assert response.status_code == 429


# verify_onetime_auth

@pytest.fixture
def onetime_auth_verification_code(db, api_client, cache, user_data):
    url = reverse("user-onetime-auth-request-auth")
    response = api_client.post(url, data=user_data)
    print([response.data, response.status_code])
    return cache.get(create_phone_verify_cache_key(user_data["phone"]))

@pytest.mark.django_db
def test_correct_verification_code_for_verifying_onetime_auth(api_client, user_data, onetime_auth_verification_code):
    url = reverse("user-onetime-auth-verify-auth-request")
    user_data["code"] = onetime_auth_verification_code
    response = api_client.post(url, data=user_data)
    assert isinstance(response.data['access'], str)
    assert isinstance(response.data['refresh'], str)

@pytest.mark.django_db
def test_incorrect_verification_code_for_verifying_onetime_auth(api_client, user_data, onetime_auth_verification_code):
    url = reverse("user-onetime-auth-verify-auth-request")
    user_data["code"] = "12345"
    response = api_client.post(url, data=user_data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_unexpected_verification_code_for_verfying_onetime_auth(api_client, user_data):
    url = reverse("user-onetime-auth-verify-auth-request")
    user_data["code"] = '12345'
    response = api_client.post(url, data=user_data)
    assert response.status_code == 400

