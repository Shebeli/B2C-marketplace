from asyncio import Server
from unittest.mock import patch

import pytest
from financeops.models import Payment
from financeops.tests.finance_factory import PaymentFactory
from product.tests.product_factory import ProductVariantFactory
from zibal.client import ZibalIPGClient
from zibal.models.schemas import (
    TransactionInquiryResponse,
    TransactionRequireResponse,
    TransactionVerifyResponse,
)

from order.models import Order
from order.tasks import cancel_unpaid_order, handle_payment
from order.tests.order_factory import OrderFactory, OrderItemFactory

# ---------------
#    Fixtures
# ---------------


@pytest.fixture
def mock_zibal_client():
    with patch("order.tasks.ZibalIPGClient") as mock_client:
        sample_response_data = {
            "message": "success",
            "result": 100,
            "refNumber": None,
            "paidAt": "2025-04-11T18:56:25.743000",
            "verifiedAt": "2025-04-11T18:56:41.377000",
            "status": 1,
            "amount": 10000,
            "orderId": "",
            "description": "",
            "cardNumber": None,
            "multiplexing_infos": [],
            "wage": 0,
            "shaparakFee": 1200,
            "createdAt": "2025-04-11T18:54:32.893000",
        }
        mock_client.inquiry_transaction.return_value = (
            TransactionInquiryResponse.from_camel_case(sample_response_data)
        )
        mock_client.request_transaction.return_value = TransactionRequireResponse(
            track_id=123, result=100, message="success"
        )
        yield mock_client.return_value


# Test tasks core logic and assert expected execution flow

PAID_AND_VERIFIED = 1


@pytest.mark.django_db
def test_handle_payment_task_succesful(mock_zibal_client):
    payment = PaymentFactory(status=Payment.UNPAID, amount=10000)

    response = mock_zibal_client.request_transaction(10000, "https://localhost.com")
    handle_payment(response.track_id, payment.id)
    payment.refresh_from_db(fields=["amount", "status"])

    assert payment.amount == 10000
    assert payment.status == Payment.PAID


@pytest.mark.django_db
def test_cancel_unpaid_order_succesful(mock_zibal_client):
    product_variants = ProductVariantFactory.create_batch(10)
    order = OrderFactory(status=Order.UNPAID)
    order_items = [
        OrderItemFactory(product_variant=variant) for variant in product_variants
    ]

    cancel_unpaid_order(order.id)

    assert order.status == Order.CANCELLED
    assert order.cancelled_by == Order.SERVER
    
    for variant in product_variants:
        assert variant.reserved_stock == 0 