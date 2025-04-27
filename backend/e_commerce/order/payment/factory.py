from django.conf import settings
from financeops.models import Payment
from order.payment.clients import ZibalIPGClient
from order.payment.exceptions import (
    PaymentGatewayNotFoundError,
    PaymentNotImplementedError,
)


class PaymentGatewayFactory:
    @staticmethod
    def get_client(selected_ipg: str):
        if selected_ipg == Payment.ZIBAL:
            return ZibalIPGClient(settings.ZIBAL_MERCHANT_ID)
        elif selected_ipg == Payment.ASAN_PARDAKHT:
            raise PaymentNotImplementedError()
        elif selected_ipg == Payment.ZIBAL:
            raise PaymentNotImplementedError()
        else:
            raise PaymentGatewayNotFoundError()