import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core import validators
import phonenumbers


def validate_phone(value: str) -> None:
    parsed_phone = phonenumbers.parse(
        value,
        "IR",
    )
    if not phonenumbers.is_valid_number(parsed_phone):
        raise ValidationError(
            _(f"Entered phone number '{value}' is not a valid phone number")
        )


def validate_username(value: str) -> None:
    "First letter should be english letter, should contain at least a total of 3 letters, minimum length is 3 and underscores are allowed"
    user_name_regex = r"^(?=[a-zA-Z])(?=(?:[^a-zA-Z]*[a-zA-Z]){3})\w{4,}$"
    pattern = re.compile(user_name_regex, re.RegexFlag.ASCII)
    if not re.search(pattern, value):
        raise ValidationError(_(f"Entered username {value} is not a valid username."))


def validate_national_code(value: str) -> None:
    validation_error = ValidationError(
        _(f"Entered national code {value} is not a valid national code.")
    )
    if not re.search(r"^\d{10}$", value):
        raise validation_error
    last_digit = int(value[-1])
    weighted_sum = sum(int(value[x]) * (10 - x) for x in range(9)) % 11
    if weighted_sum < 2:
        is_national_code_valid = last_digit == weighted_sum
    else:
        is_national_code_valid = last_digit + weighted_sum == 11
    if not is_national_code_valid:
        raise validation_error


def validate_postal_code(value: str) -> None:
    postal_code_regex = r"^(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}$"
    if not re.search(postal_code_regex, value):
        raise ValidationError(_(f"Entered postal code is not a valid postal code."))


def validate_verification_code(code: str):
    if len(code) != 5:
        raise ValidationError(_("The inputed code length isn't 5"))
    if any(digit not in "0123456789" for digit in code):
        raise ValidationError(_("The inputed code cannot contain non-digits"))
    
