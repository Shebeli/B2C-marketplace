from django.conf import settings
from financeops.models import Payment
from order.payment.clients import ZibalIPGClient
from order.payment.exceptions import (
    PaymentGatewayNotFoundError,
    PaymentNotImplementedError,
)


class PaymentGatewayFactory:
    "For creating a IPG payment client"

    @staticmethod
    def get_client(selected_ipg: int):
        """
        Creates and returns an instance of the given IPG.

        Raises:
            PaymentNotImplementedError: Given IPG is recognized but the client is not implemented yet.
            PaymentGatewayNotFoundError: Given IPG is not recognized.
        """
        ipgs = settings.IPG_CHOICES
        if selected_ipg == ipgs.ZIBAL:
            return ZibalIPGClient(settings.ZIBAL_MERCHANT_ID)
        elif selected_ipg == ipgs.ASAN_PARDAKHT:
            raise PaymentNotImplementedError()
        elif selected_ipg == ipgs.ZARIN_PAL:
            raise PaymentNotImplementedError()
        else:
            raise PaymentGatewayNotFoundError()
