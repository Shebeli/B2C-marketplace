import logging

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from ecom_core import ipg_codes
from zibal.client import ZibalIPGClient
from zibal.exceptions import RequestError, ResultError
from zibal.models.schemas import TransactionRequireResponse
from rest_framework import serializers


from financeops.models import Payment, Transaction, Wallet
from order.models import Order

logger = logging.getLogger("order")


def initiate_ipg_payment(amount: int, ipg_service: int) -> dict:
    if ipg_service == ipg_codes.ZIBAL:
        _inititate_zibal_ipg(amount)
    if ipg_service == ipg_codes.ASAN_PARDAKHT:
        raise NotImplementedError(
            "IPG gateway for AsanPardakht hasn't been implemented, yet."
        )
    else:
        raise ValueError(
            "Improper value for argument ipg_service."
            " To see the available IPG choices, please refer to ipg_codes in ecom_core django app."
        )


def _inititate_zibal_ipg(amount: int) -> TransactionRequireResponse:
    client = ZibalIPGClient(
        settings.ZIBAL_MERCHANT, raise_on_invalid_result=True, logger=logger
    )
    try:
        request_data = client.request_transaction(
            amount=amount,
            callback_url=reverse("payment-callback"),
        )
    except RequestError:
        # ZibalIPGClient uses logging to log network error
        raise serializers.ValidationError(
            "A network error has occured when connecting to zibal IPG service."
            " Please try again later."
        )
    except ResultError:
        # logger.exception(f"An unexpected `result` was received from the IPG: {exc}")
        raise serializers.ValidationError(
            "An unexpected result was received from the payment gateway service."
        )
    return request_data


def inititate_wallet_payment(
    wallet: Wallet, amount: int, ipg_service: int
) -> Transaction:
    """
    Initialize an IPG payment, update the order's status to PAYING
    and createa `Payment` instance.
    """
    request_data = initiate_ipg_payment(amount=amount, ipg_service=ipg_service)
    payment = Payment.objects.get_or_create(
        wallet=wallet,
        amount=amount,
        ipg_service=ipg_service,
        status=Payment.PAYING,
        track_id=request_data.track_id,
    )
    return payment


def initiate_order_payment(order: Order, ipg_service: int) -> Payment:
    """
    Assuming the passed in `order` arg is in UNPAID or PAYING status.

    Initialize an IPG payment, update the order's status to PAYING
    and create a `Payment` instance.
    """
    request_data = initiate_ipg_payment(amount=order.amount, ipg_service=ipg_service)
    order.status = Order.PAYING
    with transaction.atomic():
        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            ipg_service=ipg_service,
            status=Payment.PAYING,
            track_id=request_data.track_id,
        )
        order.save()
    return payment


def finalize_order_payment(payment: Payment) -> Transaction:
    """
    The passed in `Payment` instance should already be in PAID
    status. if so, then the order's status will be updated to PAID status
    with appropriate changes. Otherwise, an error will be raised.
    """
    order = payment.order
    if not order:
        raise ValueError("The payment has no order associated with it")
    if payment.status != Payment.PAID:
        raise ValueError("The payment hasn't been paid")
    if order.status != Order.PAYING:
        raise ValueError("The given order instance should be in PAYING state")
    with transaction.atomic():
        order.status = order.PAID
        order.save()
        tran = Transaction.objects.create(
            amount=order.total_price,
            type=Transaction.DIRECT_PAYMENT,
            order=order,
        )
    return tran


def finalize_wallet_payment(payment: Payment) -> Transaction:
    """
    The passed in `Payment` instance should already be in PAID status.
    if so, then the wallet's balance will increased.
    """
    wallet = payment.wallet
    if not wallet:
        raise ValueError("The payment instance has no wallet associated with it")
    if payment.status != Payment.PAID:
        raise ValueError("The payment hasn't been paid")
    if payment.is_used:
        raise ValueError("The payment has already been verified")

    with transaction.atomic():
        wallet.balance += payment.amount
        wallet.save()
        tran = Transaction.objects.create(
            amount=payment.amount, type=Transaction.DEPOSIT, wallet=wallet
        )
    return tran
