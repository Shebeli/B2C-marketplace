from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ecom_core.validators import (
    validate_phone,
    validate_username,
    validate_national_code,
    validate_postal_code,
    validate_bank_card_number,
    validate_iban,
    validate_rating,
)
from .managers import EcomUserManager


class State(models.Model):
    name = models.CharField(max_length=30)


class City(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State, on_delete=models.CASCADE)


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        "EcomUser", on_delete=models.CASCADE, related_name="profile"
    )
    wallet = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/customers/", null=True, blank=True
    )


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


class SellerProfile(models.Model):
    user = models.ForeignKey("EcomUser", on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50, unique=True, null=True)
    store_address = models.CharField(max_length=250)
    store_description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    products_sold = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        default=0.0, decimal_places=1, max_digits=5, validators=validate_rating
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/sellers/", null=True, blank=True
    )
    website = models.URLField(blank=True)
    established_date = models.DateField(
        null=True, blank=True
    )  # whenever profile is verified, this field should be inputted


class SellerProfileBusinessLicense(models.Model):
    seller_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)


class SellerProfileBankAccount(models.Model):
    seller_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, validators=validate_bank_card_number)
    card_owner_fullname = models.CharField(max_length=50, blank=True)
    iban = models.CharField(max_length=28, validators=validate_iban)


class EcomUser(AbstractBaseUser):
    "This model does not contain any superuser or staff attributes as its handled in a seperate model named 'AdminUser'"
    first_name = models.CharField(_("First Name"), max_length=50, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=50, blank=True)
    username = models.CharField(
        _("Username"),
        unique=True,
        help_text=_(
            "Maximum of 40 characters. Only letters, digits and the special character . are allowed"
        ),
        validators=[validate_username],
        error_messages={
            "null": _("The username cannot be null"),
            "blank": _("The username cannot be blank"),
            "unique": _("The username already exists"),
            "invalid": _(
                "The username is invalid. Please refer to username help text."
            ),
        },
        max_length=40,
        blank=True,
    )
    email = models.EmailField(_("Email Address"), blank=True, unique=True)
    phone = models.CharField(
        _("Phone Number"),
        max_length=13,
        validators=[validate_phone],
        unique=True,
        blank=True,
    )
    national_code = models.CharField(
        _("National Code"),
        blank=True,
        null=True,
        max_length=10,
        validators=[validate_national_code],
        unique=True,
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    balance = models.IntegerField(default=0)
    date_created = models.DateTimeField(
        _("UserAccount Creation Date"), default=timezone.now
    )

    USERNAME_FIELD = "phone"

    objects = EcomUserManager()

    # we always want a seller profile and a customer profile to be created for the user.
    # also, you might ask, why not use the django signals instead?
    # read django's own documentation warning on when to use django signals:
    # https://docs.djangoproject.com/en/5.0/topics/signals/#module-django.dispatch
    def save(self, *args, **kwargs):
        SellerProfile.objects.create(user=self)
        CustomerProfile.objects.create(user=self)
        return super().save(self, *args, **kwargs)

    @property
    def full_name(self):
        if not self.first_name and not self.last_name:
            return None
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        "To distinguish user model from admin model by using this method"
        return False

    def __str__(self):
        return f"User: {self.username} , Phone number:{self.phone}"
