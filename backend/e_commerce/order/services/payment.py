import logging

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from ecom_core import ipgs
from financeops.models import Payment, FinancialRecord, Wallet
from rest_framework import serializers
from zibal.client import ZibalIPGClient
from zibal.exceptions import RequestError, ResultError
from zibal.models.schemas import TransactionRequireResponse, TransactionVerifyResponse

from order.models import Order
from order.tasks import handle_payment

logger = logging.getLogger("order")


def initiate_ipg_payment(amount: int, ipg_service: int, base_url: str) -> dict:
    if ipg_service == ipgs.ZIBAL:
        return _inititate_zibal_payment(amount, base_url)
    elif ipg_service == ipgs.ASAN_PARDAKHT:
        raise NotImplementedError(
            "IPG gateway for AsanPardakht hasn't been implemented, yet."
        )
    else:
        raise ValueError(
            "Improper value for argument ipg_service."
            " To see the available IPG choices, please refer to ipg_codes in ecom_core django app."
            f"Available options: \n {settings.IPG_CHOICES}"
        )


def _inititate_zibal_payment(amount: int, base_url: str) -> dict:
    client = ZibalIPGClient(
        settings.ZIBAL_MERCHANT, raise_on_invalid_result=True, logger=logger
    )
    try:
        request_data = client.request_transaction(
            amount=amount,
            callback_url=base_url + reverse("zibal-callback"),
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
    return request_data.model_dump(exclude_none=True)


def initiate_wallet_payment(
    wallet: Wallet, amount: int, ipg_service: int, base_url: str
) -> FinancialRecord:
    """
    Initialize an IPG payment, update the order's status to PAYING
    and create a `Payment` model instance.
    """
    request_data = initiate_ipg_payment(
        amount=amount, ipg_service=ipg_service, base_url=base_url
    )
    payment = Payment.objects.create(
        wallet=wallet,
        amount=amount,
        ipg_service=ipg_service,
        status=Payment.PAYING,
        track_id=request_data.track_id,
    )
    handle_payment(request_data.track_id, payment.id).apply_async(
        args=(request_data.track_id, payment.id), countdown=60 * 20
    )
    return payment


def initiate_order_payment(order: Order, ipg_service: int, base_url: str) -> Payment:
    """
    Assuming the passed in `order` arg is in UNPAID or PAYING status.

    Initialize an IPG payment, update the order's status to PAYING
    and create a `Payment` instance.
    """
    request_data = initiate_ipg_payment(
        amount=order.amount, ipg_service=ipg_service, base_url=base_url
    )
    with transaction.atomic():
        order.status = Order.PAYING
        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            ipg_service=ipg_service,
            status=Payment.PAYING,
            track_id=request_data.track_id,
        )
        order.save()
    handle_payment(request_data.track_id, payment.id).apply_async(
        args=(request_data.track_id, payment.id), countdown=60 * 20
    )
    return payment


def finalize_order_payment(payment: Payment) -> FinancialRecord:
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
        tran = FinancialRecord.objects.create(
            amount=order.total_price,
            type=FinancialRecord.DIRECT_PAYMENT,
            order=order,
        )
    return tran


def finalize_wallet_payment(payment: Payment) -> FinancialRecord:
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
        tran = FinancialRecord.objects.create(
            amount=payment.amount, type=FinancialRecord.DEPOSIT, wallet=wallet
        )
    return tran
