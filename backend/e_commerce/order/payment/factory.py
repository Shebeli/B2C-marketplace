from django.conf import settings
from financeops.models import IPGChoice, Payment

from order.payment.clients import PaymentGatewayClient, ZibalIPGClient
from order.payment.exceptions import (
    PaymentGatewayNotFoundError,
    PaymentNotImplementedError,
)


class PaymentGatewayFactory:
    @staticmethod
    def get_client(ipg_choice: IPGChoice) -> PaymentGatewayClient:
        match ipg_choice:
            case Payment.ZIBAL:
                return ZibalIPGClient(settings.ZIBAL_MERCHANT_ID)
            case Payment.ZARIN_PAL:
                raise PaymentNotImplementedError()
            case Payment.ASAN_PARDAKHT:
                raise PaymentNotImplementedError()
            case _:
                raise PaymentGatewayNotFoundError()
