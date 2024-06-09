import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from ecom_user.utils import create_phone_verify_cache_key


# ---------------
#    fixtures
# ---------------


@pytest.fixture
def user_data():
    return {"phone": "09377964142"}


@pytest.fixture
def cache():
    from django.core.cache import cache

    yield cache
    cache.clear()


@pytest.fixture
def generate_user(db, django_user_model):
    def make_user(**kwargs):
        if not kwargs.get("phone"):
            kwargs["phone"] = "09377964142"
        if not kwargs.get("phone"):
            kwargs["username"] = "some_test_username"
        if not kwargs.get("password"):
            kwargs["password"] = "P@s$W0RrD$24"
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, api_client, generate_user):
    def generate_api_client(user=None):
        if not user:
            user = generate_user()
        api_client.force_authenticate(user=user)
        return api_client

    return generate_api_client


# ---------------
#   Test Cases
# ---------------


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


@pytest.fixture
def register_verification_code(db, api_client, cache, user_data):
    url = reverse("user-signup-request-registration")
    api_client.post(url, data=user_data)
    return cache.get(create_phone_verify_cache_key(user_data["phone"]))


@pytest.mark.django_db
def test_correct_code_for_verifying_register(
    api_client, register_verification_code, user_data
):
    url = reverse("user-signup-verify-registration-request")
    user_data["verification_code"] = register_verification_code
    response = api_client.post(url, data=user_data)
    assert response.status_code == 201
    assert isinstance(response.data["access"], str)
    assert isinstance(response.data["refresh"], str)


@pytest.mark.django_db
def test_incorrect_code_for_verifying_register(
    api_client, register_verification_code, user_data
):
    url = reverse("user-signup-verify-registration-request")
    user_data["verification_code"] = "12345"
    response = api_client.post(url, data=user_data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_unexpected_code_for_verifying_register(api_client, user_data):
    url = reverse("user-signup-verify-registration-request")
    user_data["verification_code"] = "12345"
    response = api_client.post(url, data=user_data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_valid_request_onetime_auth(api_client, user_data, generate_user):
    url = reverse("user-onetime-auth-request-auth")
    generate_user()
    response = api_client.post(url, data=user_data)
    assert response.status_code == 202


@pytest.mark.django_db
def test_user_too_many_onetime_auth_requests(api_client, user_data, generate_user):
    url = reverse("user-onetime-auth-request-auth")
    generate_user()
    api_client.post(url, data=user_data)
    response = api_client.post(url, data=user_data)
    assert response.status_code == 429


@pytest.fixture
def onetime_auth_verification_code(db, api_client, cache, user_data, generate_user):
    url = reverse("user-onetime-auth-request-auth")
    generate_user()
    response = api_client.post(url, data=user_data)
    print([response.data, response.status_code])
    return cache.get(create_phone_verify_cache_key(user_data["phone"]))


@pytest.mark.django_db
def test_correct_verification_code_for_verifying_onetime_auth(
    api_client, user_data, onetime_auth_verification_code
):
    url = reverse("user-onetime-auth-verify-auth-request")
    user_data["verification_code"] = onetime_auth_verification_code
    response = api_client.post(url, data=user_data)
    assert response.status_code == 200
    assert isinstance(response.data["access"], str)
    assert isinstance(response.data["refresh"], str)


@pytest.mark.django_db
def test_incorrect_verification_code_for_verifying_onetime_auth(
    api_client, user_data, onetime_auth_verification_code
):
    url = reverse("user-onetime-auth-verify-auth-request")
    user_data["verification_code"] = "123456"
    response = api_client.post(url, data=user_data)
    assert response.status_code == 400
    assert response.data == {"error": "verification code is incorrect"}


@pytest.mark.django_db
def test_unexpected_verification_code_for_verfying_onetime_auth(api_client, user_data):
    url = reverse("user-onetime-auth-verify-auth-request")
    user_data["verification_code"] = "123456"
    response = api_client.post(url, data=user_data)
    assert response.status_code == 400
    assert response.data == {
        "error": "server is not expecting a verification code for this phone"
    }


@pytest.mark.django_db
def test_correct_password_change(api_client_with_credentials, generate_user):
    current_password = "123456AbC!@#"
    new_password = "382u13#!@FDAS"
    user = generate_user(password=current_password)
    api_client = api_client_with_credentials(user)
    url = reverse("user-account-change-password")
    request_data = {
        "old_password": current_password,
        "new_password": new_password,
        "new_password_verify": new_password,
    }
    response = api_client.put(url, data=request_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_updating_trivial_account_info(api_client_with_credentials):
    api_client = api_client_with_credentials()
    request_data = {
        "first_name": "John",
        "last_name": "Cena",
        "username": "JohnFreakingCena",
        "email": "JohnCena123@gmail.com",
    }
    url = reverse("user-account-update-info")
    response = api_client.put(url, request_data)
    assert response.status_code == 200
    # check to see if the account info got updated
    url = reverse("user-account-get-info")
    response = api_client.get(url)
    print(response.data)
    assert response.status_code == 200
    assert response.data["first_name"] == "John"


@pytest.mark.django_db
def test_phone_change_process(api_client_with_credentials, cache):
    # first, submit a request for changing the phone number.
    api_client = api_client_with_credentials()
    new_phone = "09377964143"
    change_phone_request_data = {"phone": new_phone}
    url = reverse("user-account-change-phone-request")
    response = api_client.put(url, change_phone_request_data)
    assert response.status_code == 202
    # second, verify the new phone using the verification code which has been sent via SMS.
    verification_code = cache.get(create_phone_verify_cache_key(new_phone))
    url = reverse("user-account-change-phone-verify")
    change_phone_verify_data = {
        "phone": new_phone,
        "verification_code": verification_code,
    }
    response = api_client.put(url, change_phone_verify_data)
    assert response.status_code == 200
    # and for the last step, check to see if the phone number was updated.
    url = reverse("user-account-get-info")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["phone"] == new_phone
