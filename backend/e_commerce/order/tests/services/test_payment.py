from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from ecom_core import ipgs
from rest_framework.exceptions import ValidationError
from zibal.client import ZibalIPGClient
from zibal.exceptions import RequestError, ResultError
from zibal.models.schemas import TransactionRequireResponse

from order.services.payment import (
    finalize_order_payment,
    finalize_wallet_payment,
    initiate_ipg_payment,
    initiate_order_payment,
    initiate_wallet_payment,
)

# initate_ipg_payment tests:


@pytest.fixture
def mock_client():
    with patch("order.services.payment.ZibalIPGClient") as MockClient:
        yield MockClient.return_value


def test_initiate_ipg_payment_zibal_success(mock_client):
    expected_response = TransactionRequireResponse(
        track_id=123, result=100, message="success"
    )
    mock_client.request_transaction.return_value = expected_response
    base_url = "https://localhost.com"
    response = initiate_ipg_payment(5000, ipgs.ZIBAL, base_url=base_url)  # 1 for zibal

    assert response == {
        "track_id": 123,
        "result": 100,
        "message": "success",
    }
    callback_url = base_url + reverse("zibal-callback")
    mock_client.request_transaction.assert_called_once_with(
        amount=5000, callback_url=callback_url
    )


# -----------------
#   Failure cases
# -----------------


def test_inititate_ipg_payment_zibal_not_implemented_error():
    with pytest.raises(NotImplementedError):
        initiate_ipg_payment(
            amount=2000,
            ipg_service=ipgs.ASAN_PARDAKHT,
            base_url="https://localhost.com",
        )


def test_inititate_ipg_payment_zibal_value_error():
    with pytest.raises(ValueError):
        initiate_ipg_payment(
            amount=2000, ipg_service=12, base_url="https://localhost.com"
        )


def test_zibal_ipg_request_error(mock_client):
    mock_client.request_transaction.side_effect = RequestError

    with pytest.raises(ValidationError):
        initiate_ipg_payment(5000, ipgs.ZIBAL, base_url="https://localhost.com")


def test_zibal_ipg_result_error(mock_client):
    mock_client.request_transaction.side_effect = ResultError

    with pytest.raises(ValidationError):
        initiate_ipg_payment(5000, ipgs.ZIBAL, base_url="https://localhost.com")


# initiate_wallet_payment tests:


def wallet_payment_inititate(mock_client, customer_and_seller):
    customer, seller = customer_and_seller
    initiate_wallet_payment(
        customer.wallet, 5000, ipgs.ZIBAL, base_url="https://localhost.com"
    )
