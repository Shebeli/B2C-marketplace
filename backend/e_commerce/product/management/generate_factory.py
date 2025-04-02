import itertools

import factory
from ecom_user.models import EcomUser
from factory.django import DjangoModelFactory

ecom_user = EcomUser.objects.order_by("-id").first()
if ecom_user:
    phone_counter = itertools.count(int(ecom_user.phone[1:]) + 1)
else:
    phone_counter = itertools.count(9000000000)


def generate_unique_phone():
    return f"0{next(phone_counter)}"


class FakeUserFactory(DjangoModelFactory):
    "For generating data which is intended to be persistent for testing purposes on local development machines."

    class Meta:
        model = EcomUser

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.LazyFunction(generate_unique_phone)
