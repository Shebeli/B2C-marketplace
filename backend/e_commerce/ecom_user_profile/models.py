from django.db import models
from django.core.cache import cache

from django.utils.translation import gettext_lazy as _
from django.core import exceptions

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

    
    # def verify_eligiblity(self):
    #     redis_client = cache.client.get_client()
    #     required_fields = redis_client.smembers("seller_required_fields")
    #     if not required_fields:
    #         required_fields = ["store_name", "store_description", "store_address"]
    #         redis_client.sadd("seller_required_fields", required_fields)
    #     for field_name in required_fields:
    #         self.
    #         field = getattr(self, field_name)
    #         if not field:
    #             raise exceptions.ValidationError(
    #                 f"The field '{field}' doesn't exist on the SellerProfile model"
    #             )
                
            


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
