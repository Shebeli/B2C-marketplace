from django.db import models

from django.utils.translation import gettext_lazy as _

from ecom_core.validators import (
    validate_iban,
    validate_bank_card_number,
    validate_postal_code,
    validate_rating,
)


class State(models.Model):
    name = models.CharField(max_length=30)


class City(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State, on_delete=models.CASCADE)


CUSTOMER_PROFILE_DEFAULT_PREFERENCES = {
    "notifications": {"email": True, "sms": True, "frequency": "1/week"},
    "display": {"theme": "light", "language": "fa"},
    "shopping": {
        "favorite_products": [],
        "favorite_sellers": [],
    },
    "privacy": {
        "is_profile_public": True,
    },
}


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        "ecom_user.EcomUser", on_delete=models.CASCADE, related_name="customer_profile"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/customers/", null=True, blank=True
    )
    preferences = models.JSONField(blank=True, null=True)


class CustomerAddress(models.Model):
    user = models.ForeignKey(
        "ecom_user.EcomUser",
        on_delete=models.CASCADE,
        related_name="customer_addresses",
    )
    address = models.CharField(max_length=250)
    postal_code = models.CharField(
        _("Postal Code"),
        null=True,
        max_length=10,
        validators=[validate_postal_code],
        unique=True,
    )


class SellerProfile(models.Model):
    user = models.ForeignKey(
        "ecom_user.EcomUser", on_delete=models.CASCADE, related_name="seller_profile"
    )
    store_name = models.CharField(max_length=50, unique=True, null=True)
    store_address = models.CharField(max_length=250)
    store_description = models.CharField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    products_sold = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        default=0.0, decimal_places=1, max_digits=5, validators=[validate_rating]
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/sellers/", null=True, blank=True
    )
    website = models.URLField(blank=True)
    established_date = models.DateField(
        null=True, blank=True
    )  # whenever profile is verified, this field should be inputted


class SellerBusinessLicense(models.Model):
    user = models.ForeignKey(
        "ecom_user.EcomUser",
        on_delete=models.CASCADE,
        related_name="seller_business_licenses",
    )
    submitted_date = models.DateTimeField(auto_now_add=True)
    license_picture = models.ImageField(upload_to="business_licenses/")


class SellerBankAccount(models.Model):
    user = models.ForeignKey(
        "ecom_user.EcomUser",
        on_delete=models.CASCADE,
        related_name="seller_bank_accounts",
    )
    card_number = models.CharField(
        max_length=16, validators=[validate_bank_card_number]
    )
    card_owner_fullname = models.CharField(max_length=50)
    iban = models.CharField(max_length=28, validators=[validate_iban])
