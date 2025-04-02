import itertools

import factory
from ecom_user.models import EcomUser
from factory.django import DjangoModelFactory

phone_counter = None


def generate_phone():
    global phone_counter
    if phone_counter is None:
        ecom_user = EcomUser.objects.order_by("-id").first()
        start_number = int(ecom_user.phone[1:]) + 1 if ecom_user else 9000000002
        phone_counter = itertools.count(start_number)

    return f"0{next(phone_counter)}"


class CustomerFactory(DjangoModelFactory):
    "A customer profile is created when an ecomuser instance is created."

    class Meta:
        model = EcomUser

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.LazyFunction(generate_phone)


class SellerFactory(DjangoModelFactory):
    "A seller profile is created when an ecomuser instance is created."

    class Meta:
        model = EcomUser

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.LazyFunction(generate_phone)
