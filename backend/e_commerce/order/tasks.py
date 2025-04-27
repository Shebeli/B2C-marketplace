from datetime import timedelta, timezone
import logging

import requests
from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from financeops.models import IPG, FinancialRecord, Payment
from order.utils import format_time
from product.models import ProductVariant
from requests.exceptions import RequestException

from order.models import Order
from order.payment.exceptions import PaymentRequestError, PaymentResponseError
from order.payment.factory import PaymentGatewayFactory
from order.payment.schemas import PAYMENT_STATUS_CODES

logger = logging.getLogger("order")


# @shared_task(bind=True, max_retries=5, default_retry_delay=45)
# def handle_payment(self, track_id: int, payment_id: int, status_code: int) -> None:
#     try:
#         payment = Payment.objects.get(id=payment_id)
#     except Payment.DoesNotExist:
#         logger.error(
#             f"Failed to resolve given payment object using payment_id: {payment_id} "
#             f"from the database in the following task: \n"
#             f"task ID: {self.task.id} | task name: {self.request.task}"
#         )
#         return

#     # payment is paid most likely, so no need for inquiring
#     if payment.status not in (Payment.UNPAID, Payment.PAYING):
#         logger.info(
#             f"The order with id of {payment} is no longer in UNPAID or PAYING status \n"
#             f"Order's current status: {payment.status} \n"
#             f"No further call to the IPG will be made for syncing the status of payment."
#         )
#         return

#     # order is still unpaid, inquiring to update the payment object.
#     try:
#         payment_client = PaymentGatewayFactory.get_client(payment.ipg_service)
#     except Exception as e:
#         logger.error(
#             f"Failed to retrieve the payment client via the client associated with payment object with id of {payment.id}"
#             "inside the task `handle_payment`. | "
#             f"error details: {str(e)}"
#         )
#     try:
#         response_data = payment_client.inquiry_transaction(track_id=track_id)
#         if response_data.status == 1:  # paid and unverified
#             verify_data = payment_client.verify_transaction(track_id)
#             payment.paid_amount = verify_data.amount
#             payment.status = Payment.PAID
#         elif response_data.status == 2:  # paid and verified
#             payment.paid_amount = response_data.amount
#             payment.status = Payment.PAID
#         else:
#             payment.status = Payment.CANCELLED
#         payment.details = PAYMENT_STATUS_CODES.get(
#             response_data.status,
#             f"No status message mapping was found for given status code: {response_data.status}",
#         )
#         payment.save()
#     except PaymentRequestError as exc:
#         raise self.retry(exc=exc)
#     except PaymentResponseError as exc:
#         logger.error(
#             f"Unexpected response received from the IPG webserver when inquiring/verifying transaction inside of handle_payment task. | "
#             f"payment_id: {payment_id} | error: {str(exc)}"
#         )


@shared_task(bind=True, max_retries=6, default_retry_delay=15)
def handle_payment(self, track_id: int, payment_id: int) -> None:
    """
    For verifying the transaction via server-to-server method.
    """
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        logger.error(
            f"Failed to resolve given payment object using payment_id: {payment_id} "
            f"from the database in the following task: \n"
            f"task ID: {self.task.id} | task name: {self.request.task}"
        )
        return

    try:
        payment_client = PaymentGatewayFactory.get_client(payment.ipg_service)
    except Exception as e:
        logger.error(
            f"Failed to retrieve the payment client via the client associated with payment object with id of {payment.id}"
            "inside the task `handle_payment`. | "
            f"error details: {str(e)}"
        )

    try:
        response = payment_client.inquiry_transaction(track_id)
        if response.status == 1:  # paid and unverified
            verify_data = payment_client.verify_transaction(track_id)
            payment.paid_amount = verify_data.amount
            payment.status = Payment.PAID
        elif response.status == 2:  # paid and verified
            payment.status = Payment.PAID
        else:
            payment.status = Payment.FAILED
        if response.status_meaning:
            payment.details = response.status_meaning
        payment.save()
    except PaymentRequestError as exc:
        raise self.retry(exc=exc)
    except PaymentResponseError as exc:
        logger.error(
            f"Unexpected response received from the IPG webserver when verifying/inquiring transaction inside of handle_payment task. | "
            f"payment_id: {payment_id} | error: {str(exc)}"
        )


@shared_task
def cancel_payment(payment_id: int):
    """
    Cancel the given payment object which are still in PAYING status by updating
    its state to CANCELLED.
    """
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        logger.error(
            f"Failed to resolve given payment object using payment_id: {payment_id} "
            f"from the database in the following task: \n"
        )
        return

    if payment.status == Payment.PAYING:
        logger.info(
            f"Payment with id of {payment.id} is still in paying state, updating the status to CANCELLED."
        )
        payment.status = Payment.CANCELLED
        payment.save()


@shared_task(bind=True, max_retries=5, default_retry_delay=75)
def cancel_unpaid_order(self, order_id):
    """
    For cancelling orders which haven't been paid for about 1-2 hours,
    which will also release the reserved stocks occupied by the order.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.error(
            f"Failed to resolve given order object using order_id: {order_id} "
            f"from the database in the following task: \n"
            f"task ID: {self.task.id} | task name: {self.request.task}"
        )
        return

    # if order is expired, release the stocks and update the order
    if timezone.now() > order.expire_timestamp:
        with transaction.atomic():
            product_variants = []
            for order_item in order.items.all():
                product_variant = order_item.product_variant
                product_variant.reserved_stock -= order_item.quantity
                product_variant.on_hand_stock += order_item.quantity
                product_variants.append(product_variant)
            order.status = Order.TIMED_OUT
            ProductVariant.objects.bulk_update(
                product_variants, ["reserved_stock", "on_hand_stock"]
            )
            order.save()
        logger.info(
            f"The order with id of {order.id} is timed out and the reserved stocks are released."
        )
        return

    # retrieve the latest payment object and conduct whether a payment
    # is still going on. if so, retry the current task based on the remaining
    # time of the payment.
    if order.status == Order.PAYING:
        remaining_payment_time = (
            timezone.now() - timedelta(minutes=15)
        ) - order.payment.track_id_submitted_at

        formatted_time = format_time(remaining_payment_time)

        logger.info(
            f"Order with id of {order.id} is in PAYING status with remaining time {formatted_time}"
            f"Remaining time on the order is in {formatted_time}"
        )
        raise self.retry(countdown=remaining_payment_time)  # retry in 20 minutes
    if order.status == Order.UNPAID:
        with transaction.atomic():
            product_variants = []
            for order_item in order.items.all():
                product_variant = order_item.product_variant
                product_variant.reserved_stock -= order_item.quantity
                product_variant.on_hand_stock += order_item.quantity
                product_variants.append(product_variant)
            order.status = Order.CANCELLED
            order.cancelled_by = Order.SERVER
            order.cancel_reason = "Cancelled by server due to order not getting paid."
            ProductVariant.objects.bulk_update(
                product_variants, ["reserved_stock", "on_hand_stock"]
            )
            order.save()


@shared_task(bind=True)
def update_order_to_delivered(self, order_id: int):
    """
    After a period of 5 business days of shipment, if no complaints have been
    recieved from the customer, the order's status is updated to DELIVERED.

    However, if the order is not delivered and the customer
    informs the server that the order hasn't been delivered,
    customer support should intervene and check what has happened
    with the order, and should follow up with approprite actions
    inorder to resolve the issue, and update the order and related data models
    accordingly.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.error(
            f"Failed to resolve given order object using order_id: {order_id} "
            f"from the database in the following task: \n"
            f"task ID: {self.task.id} | task name: {self.request.task}"
        )
        return
    commission_rate = settings.COMMISSION_RATE
    seller_wallet = order.seller.wallet
    with transaction.atomic():
        FinancialRecord.objects.create(
            type=FinancialRecord.ORDER_REVENUE,
            commission_rate=commission_rate,
            order=order,
            amount=order.total_price * commission_rate,
        )
        seller_wallet += order.total_price * commission_rate
        seller_wallet.save()
        order.status = Order.DELIVERED
        order.save()


@shared_task
def check_and_cache_ipg_status():
    """
    Cache the available ipgs with a get request to assert whether the IPG
    service is running or not.
    """
    ipgs = IPG.objects.all()
    if not ipgs:
        logger.critical(
            "One IPG instance should at least exist for IPG status scheduler checker."
        )
        return
    available_ipgs = []
    for ipg in IPG.objects.all():
        try:
            response = requests.get(ipg.status_check_url, timeout=5)
            if response.status_code != 200:
                logger.warning(
                    f"Unexpected response status code on service check: {response.status_code} content: {response.content}"
                    f"\n IPG service {ipg.service_name} is unavailable, disabling gateway."
                )
                return

        except RequestException as err:
            logger.warning(
                f"A network request error has occured on IPG status check: {err}"
                f"\n IPG service {ipg.service_name} is unavailable, disabling gateway."
            )
            return
        available_ipgs.append(ipg.id)
    cache.set("available_ipgs", available_ipgs)
