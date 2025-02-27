import re
from string import digits

import phonenumbers
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumbers import NumberParseException
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


def validate_phone(value: str) -> None:
    if re.search(r"\D", value):
        raise ValidationError(
            _(f"Entered phone number '{value}' is not a valid phone number")
        )
    try:
        parsed_phone = phonenumbers.parse(
            value,
            "IR",
        )
    except NumberParseException:
        raise ValidationError(
            _(f"Entered phone number '{value}' is not a valid phone number")
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
        raise ValidationError(_("Entered postal code is not a valid postal code."))


def validate_verification_code(code: str) -> None:
    expected_code_length = settings.OTP_LENGTH
    if len(code) != expected_code_length:
        raise ValidationError(
            _(f"The inputed code length isn't {expected_code_length}")
        )
    if any(digit not in digits for digit in code):
        raise ValidationError(_("The inputed code cannot contain non-digits"))


def validate_token_type(token: RefreshToken, expected_user_type: str) -> None:
    if token.get("user_type") != expected_user_type:
        raise TokenError("Provided token doesn't contain the expected user type claim")


def validate_bank_card_number(card_number: str) -> None:
    if len(card_number) != 16:
        raise ValidationError("Provided bank card number length should be 16")
    r = [
        (1 if (i + 1) % 2 == 0 else 2) * int(card_number[i])
        for i in range(len(card_number))
    ]
    r = [(i - 9 if i > 9 else i) for i in r]
    if not sum(r) % 10 == 0:
        raise ValidationError("Provided bank card number is not valid")


def validate_iban(iban: str) -> None:  # IR062960000000100324200001
    if len(iban) != 26:
        raise ValidationError("Provided IBAN length should be 26")
    character_map = {
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15,
        "G": 16,
        "H": 17,
        "I": 18,
        "J": 19,
        "K": 20,
        "L": 21,
        "M": 22,
        "N": 23,
        "O": 24,
        "P": 25,
        "Q": 26,
        "R": 27,
        "S": 28,
        "T": 29,
        "U": 30,
        "V": 31,
        "W": 32,
        "X": 33,
        "Y": 34,
        "Z": 35,
    }
    iban_letters = list(iban)[4:]
    for letter in iban[:4]:
        if letter in character_map.keys():
            first_digit, second_digit = list(
                str(character_map[letter])
            )  # e.g. 12 -> ['1','2']
            iban_letters.append(first_digit)
            iban_letters.append(second_digit)
        else:
            iban_letters.append(letter)
    if not int("".join(iban_letters)) % 97 == 1:
        raise ValidationError("Provided IBAN isn't valid")


def validate_rating(rating: float) -> None:
    if not 1 <= rating <= 5:
        raise ValidationError("Provided rating should be between 1 and 5")
