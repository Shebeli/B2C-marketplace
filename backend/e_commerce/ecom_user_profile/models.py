import datetime
import logging
from typing import List

from django.conf import settings
from django.core import exceptions
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from ecom_core.validators import (
    validate_bank_card_number,
    validate_iban,
    validate_postal_code,
    validate_rating,
)

# Instead of storing any extra information or preferences for the customer in
# a table field or column, a more flexible way to store them is to instead
# use a JSON field.
# The following constant is a template for the JSON field,
# which holds the most common information or preferences for each customer
# for this web application and is subject to change at any given time.

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
    birth_date = models.DateField(blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True)
    wishlist = models.ManyToManyField(
        "product.Product", related_name="wishlisted_by", blank=True
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
    user = models.OneToOneField(
        "ecom_user.EcomUser", on_delete=models.CASCADE, related_name="seller_profile"
    )
    store_name = models.CharField(max_length=50, unique=True, null=True)
    store_address = models.CharField(max_length=250)
    store_description = models.CharField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    products_sold = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        default=0.0, max_digits=1, decimal_places=1, validators=[validate_rating]
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/sellers/", null=True, blank=True
    )
    website = models.URLField(blank=True)
    established_date = models.DateField(
        null=True, blank=True
    )  # whenever profile is verified, this field will be inputted.

    # If the seller is trying to verify their eligibilty for the first time,
    # validate their eligibility, then their seller account status will be verified by updating
    # their associated  fields.
    # However, if the eligbility required fields gets changed during production,
    # all sellers who have been already verified will have their eligibility revalidated,
    # and if they are not eligible anymore, their verification field 'is_verified' will
    # be set to False.

    def reverify_verified_sellers(self) -> None:
        "After the seller required fields are changed by an EcomAdmin, this method should be called."
        verified_sellers = self.objects.filter(is_verified=True)
        for seller in verified_sellers:
            try:
                seller._validate_eligibility()
            except exceptions.ValidationError as e:
                seller.is_verified = False
                seller.save()
                logging.warning(e, exc_info=True)

    def verify_eligibility(self) -> None:
        "Will update the seller's fields established_date and is_verified if no exception is raised"
        self._validate_eligibility()
        self._update_eligible_seller_fields()

    def _update_eligible_seller_fields(self) -> None:
        "Should be called only when seller has been verified"
        if not self.established_date:
            self.established_date = datetime.date.today()
        self.is_verified = True
        self.save(update_fields=["established_date", "is_verified"])

    def _validate_eligibility(self) -> None:
        required_fields = self._get_required_seller_fields()
        self._validate_seller_required_fields(required_fields)

    # Required fields are retrieved from cache, which is subject to change by admins at any given time.
    def _get_required_seller_fields(self) -> List[str]:
        redis_client = cache.client.get_client()
        required_fields = redis_client.smembers("seller_required_fields")
        if not required_fields:
            return settings.DEFAULT_REQUIRED_SELLER_FIELDS
        return [field.decode() for field in required_fields]

    def _validate_seller_required_fields(self, required_fields: List[str]) -> None:
        invalid_field_names = self._get_invalid_field_names(required_fields)
        valid_field_names = [
            field for field in required_fields if field not in invalid_field_names
        ]
        empty_fields = self._get_empty_fields(valid_field_names)
        errors = {}
        if invalid_field_names:
            errors["invalid_fields"] = (
                f"The following field(s) doesn't exist on EcomUser: {", ".join(invalid_field_names)}"
            )
        if empty_fields:
            errors["empty_fields"] = (
                f"The following field(s) are empty or null: {", ".join(empty_fields)}"
            )
        if errors:
            raise exceptions.ValidationError(errors)

    def _get_invalid_field_names(self, field_names: List[str]) -> List[str]:
        valid_field_names = [field.name for field in self._meta.get_fields()]
        return valid_field_names

    def _get_empty_fields(self, field_names: List[str]) -> List[str]:
        empty_fields = [field for field in field_names if not getattr(self, field)]
        return empty_fields


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
