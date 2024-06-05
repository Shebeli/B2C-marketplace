from django.db import models
from django.utils.translation import gettext_lazy as _

from ecom_core.validators import (
    validate_bank_card_number,
    validate_iban,
    validate_rating,
)


class SellerProfile(models.Model):
    shop_address = models.CharField(max_length=250, blank=True)
    balance = models.IntegerField(default=0)
    is_eligible = models.BooleanField(default=False)
    products_sold = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        default=0, decimal_places=1, max_digits=5, validators=validate_rating
    )


class SellerProfileBankAccount(models.Model):
    seller_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    card = models.CharField(max_length=16, validators=validate_bank_card_number)
    iban = models.CharField(max_length=28, validators=validate_iban)
