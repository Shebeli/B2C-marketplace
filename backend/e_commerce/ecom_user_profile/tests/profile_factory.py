import factory
from ecom_user.models import EcomUser
from factory.django import DjangoModelFactory


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = EcomUser
        django_get_or_create = ("phone",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = "09377964248"


class SellerFactory(DjangoModelFactory):
    class Meta:
        model = EcomUser
        django_get_or_create = ("phone",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = "09377966969"
