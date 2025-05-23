import logging
from abc import ABC, abstractmethod

from django.conf import settings
from django.urls import reverse
from financeops.models import Payment
from order.payment.schemas import PaymentRequestResponse, PaymentStatusResponse
from payment.exceptions import (
    PaymentGatewayNotFoundError,
    PaymentNotImplementedError,
    PaymentRequestError,
    PaymentResponseError,
)
from zibal.client import ZibalIPGClient as ZibalClient
from zibal.exceptions import RequestError, ResultError


# An interface for implementing payment clients
class PaymentGatewayClient(ABC):
    def __init__(self, service_name: str, logger=None, *args, **kwargs):
        self.service_name = service_name
        self.logger = logger or logging.getLogger(f"payment.{service_name}")

    @abstractmethod
    def request_transaction(
        self, amount: int, callback_url: str
    ) -> PaymentRequestResponse:
        pass

    @abstractmethod
    def verify_transaction(self, track_id: int) -> PaymentStatusResponse:
        pass

    @abstractmethod
    def inquiry_transaction(self, track_id: int) -> PaymentStatusResponse:
        pass

    @abstractmethod
    def get_payment_link(self, track_id: int) -> str:
        pass

    @abstractmethod
    def check_health(self) -> bool:
        pass


class ZibalIPGClient(PaymentGatewayClient):
    def __init__(self, merchant_id: str, logger=None, client=None):
        self.zibal_client = client or ZibalClient(
            merchant_id, raise_on_invalid_result=True, request_timeout=4
        )
        super().__init__(logger)

    def _handle_error(self, e: Exception) -> None:
        if isinstance(e, ResultError):
            self.logger.error(
                f"Bad response received from ZibalIPG for transaction request: {str(e)}"
            )
            raise PaymentResponseError()
        else:
            self.logger.error(
                f"Error in ZibalIPG transaction request HTTP request: {str(e)}"
            )
            raise PaymentRequestError()

    def request_transaction(self, amount, callback_url) -> PaymentRequestResponse:
        try:
            response = self.zibal_client.request_transaction(
                amount, callback_url=callback_url
            )
        except Exception as e:
            self._handle_error(e)

        return PaymentRequestResponse(
            result_code=response.result,
            result_meaning=response.result_meaning,
            track_id=response.track_id,
        )

    def verify_transaction(self, track_id) -> PaymentStatusResponse:
        try:
            response = self.zibal_client.verify_transaction(track_id)
        except Exception as e:
            self._handle_error(e)

        return PaymentStatusResponse(
            status=response.status,
            paid_at=response.paid_at,
            status_meaning=response.status_meaning,
            amount=response.amount,
            ref_number=response.ref_number,
            description=response.description,
            order_id=response.order_id,
        )

    def inquiry_transaction(self, track_id):
        try:
            response = self.zibal_client.inquiry_transaction(track_id)
        except Exception as e:
            self._handle_error(e)

        return PaymentStatusResponse(
            status=response.status,
            paid_at=response.paid_at,
            status_meaning=response.status_meaning,
            amount=response.amount,
            ref_number=response.ref_number,
            description=response.description,
            order_id=response.order_id,
        )

    def get_payment_link(self, track_id) -> str:
        return self.zibal_client.create_payment_link(track_id)


    def check_health(self) -> bool:
        return self.zibal_client.check_service_status()


class ZarinPalIPGClient(PaymentGatewayClient):
    pass


class AsanPardakhtIPGClient(PaymentGatewayClient):
    pass
