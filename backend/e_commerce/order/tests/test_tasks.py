import pytest

from financeops.models import Payment
from order.tasks import handle_payment
from zibal.models.schemas import TransactionInquiryResponse

# ---------------
#    Fixtures
# ---------------


@pytest.fixture
def payment_factory():
    def create_payment_obj():
        return Payment.objects.create(status=Payment.PAYING)

    return create_payment_obj


@pytest.fixture
def mocked_succesful_payment_handling(mocker):
    return mocker.patch("order.tasks.handle_payment", return_value=None)


@pytest.fixture
def mock_zibal_client(mocker):
    with mocker.patch("order.services.payment.ZibalIPGClient") as MockClient:
        yield MockClient.return_value


# handle_payment tests

PAID_AND_VERIFIED = 1

@pytest.mark.django_db
def test_paid_and_verified_payment_handling(
    mock_zibal_client, mocked_succesful_payment_handling, payment_factory
):
    payment = payment_factory()
    sample_response_data = {
        "message": "success",
        "result": 100,
        "ref_number": None,
        "paid_at": None,
        "verified_at": None,
        "status": -1,
        "amount": 50000,
        "order_id": "",
        "description": "",
        "card_number": None,
        "multiplexing_infos": [],
        "wage": 0,
        "shaparak_fee": 1200,
        "created_at": "2024-12-02T20:09:10.637000",
    }
    mock_zibal_client.inquiry_transaction.return_value = TransactionInquiryResponse(
        **sample_response_data
    )
    handle_payment.delay(payment_id=payment.id, track_id=100)
    mocked_succesful_payment_handling.assert_called_once_with(
        payment_id=payment.id, track_id=100
    )
    payment.refresh_from_db()
