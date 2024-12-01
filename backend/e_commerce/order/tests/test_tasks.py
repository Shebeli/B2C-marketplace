import pytest

from financeops.models import Payment
from order.tasks import handle_payment

@pytest.fixture
def payment_factory():
    return Payment.objects.create(status=Payment.PAYING)

@pytest.mark.django_db
def test_handle_succesful_payment()
    