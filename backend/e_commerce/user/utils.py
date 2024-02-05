from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import phonenumbers


def validate_phone(value):
    "The phone numbers country is assumed to be IR"
    pass