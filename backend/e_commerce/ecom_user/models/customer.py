from django.db import models
from django.utils.translation import gettext_lazy as _

from ecom_core.validators import validate_postal_code
from .core import EcomUser


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        EcomUser, on_delete=models.CASCADE, related_name="profile"
    )
    wallet = models.PositiveIntegerField(default=0)


class CustomerProfileAddress(models.Model):
    customer_profile = models.ForeignKey(
        CustomerProfile, on_delete=models.CASCADE, related_name="addresses"
    )
    address = models.CharField(max_length=250)
    postal_code = models.CharField(
        _("Postal Code"),
        null=True,
        max_length=10,
        validators=[validate_postal_code],
        unique=True,
    )
