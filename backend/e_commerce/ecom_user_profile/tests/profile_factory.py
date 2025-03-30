import itertools

import factory
from ecom_user.models import EcomUser
from factory.django import DjangoModelFactory

phone_counter = itertools.count(9000000000)


def generate_unique_phone():
    return f"09{next(phone_counter)}"


class CustomerFactory(DjangoModelFactory):
    "A customer profile is created when an ecomuser instance is created."

    class Meta:
        model = EcomUser

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.LazyFunction(generate_unique_phone)


class SellerFactory(DjangoModelFactory):
    "A seller profile is created when an ecomuser instance is created."

    class Meta:
        model = EcomUser

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.LazyFunction(generate_unique_phone)
