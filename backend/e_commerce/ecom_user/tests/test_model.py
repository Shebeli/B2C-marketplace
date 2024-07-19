import pytest

from django.core.exceptions import ValidationError

from ecom_core.validators import validate_postal_code
from ecom_user.models import EcomUser
from ecom_user.exceptions import CommandNotAllowedException

# ---------------
#    Fixtures
# ---------------


# ---------------
#   Test Cases
# ---------------


@pytest.mark.django_db
def test_createsuperuser_raises_exception():
    with pytest.raises(CommandNotAllowedException):
        EcomUser.objects.create_superuser()


@pytest.mark.django_db
@pytest.mark.parametrize("postal_code", ["1653879533", "1653879531"])
def test_user_valid_postal_codes(postal_code):
    user = EcomUser.objects.create_user(username="test_user")
    user.postal_code = postal_code
    user.clean_fields()
    user.save()
    assert user.postal_code == postal_code


@pytest.mark.django_db
@pytest.mark.parametrize("postal_code", ["73432847932", "83427492", "1111879531"])
def test_invalid_postal_codes(postal_code):
    with pytest.raises(ValidationError):
        validate_postal_code(postal_code)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username", ["john123", "JOHN", "shambile_21meow", "Mike_1234", "A_Z_O", "S__ob"]
)
def test_user_valid_username(username):
    user = EcomUser.objects.create_user(username=username)
    user.clean_fields()
    user.save()
    assert user.username == username


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username",
    [
        "john_123@!",
        "ewqیبسشیشdfasdیسش",
        "][][][#@!#!",
        "-",
        " f r q r _ 1 23",
        ".",
        "_._-",
        "12erq",
    ],
)
def test_user_invalid_username(username):
    with pytest.raises(ValidationError):
        user = EcomUser.objects.create_user(username=username)
        user.clean_fields()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "phone", ["091232132131", "9898321313", "377974148", "091299999998"]
)
def test_user_invalid_phone(phone):
    with pytest.raises(ValidationError):
        user = EcomUser.objects.create_user(phone=phone)
        user.clean_fields()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "phone", ["09377964142", "9377964142", "989377964142", "+989377964142"]
)
def test_user_phone_normalization(phone):
    user = EcomUser.objects.create_user(
        "Mike", phone, "Mikesbastion@gmail.com", "MikesPassword"
    )
    assert user.phone == "09377964142", "Check if phone is normalized"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "national_code", ["0023070072", "0034549757", "0033303002", "5317163188"]
)
def test_user_valid_nationalcode(national_code):
    user = EcomUser.objects.create_user("Mike", "09377964148")
    user.national_code = national_code
    user.clean_fields()
    user.save()
    assert user.national_code == national_code, "No validation errors should be raised"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "national_code", ["1234567890", "0023070071", "0033203001", "53171631828"]
)
def test_user_invalid_nationalcode(national_code):
    with pytest.raises(ValidationError):
        user = EcomUser.objects.create_user("Mike", "09377964148")
        user.national_code = national_code
        user.clean_fields()
