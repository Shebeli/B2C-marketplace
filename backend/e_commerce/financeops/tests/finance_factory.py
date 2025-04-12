import factory
from ecom_user_profile.tests.profile_factory import CustomerFactory, SellerFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from financeops.models import Payment


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    status = Payment.PAID
    paid_by = factory.SubFactory(CustomerFactory)
    amount = FuzzyInteger(1000, 9999999)
