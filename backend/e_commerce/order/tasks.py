import logging

from django.db import transaction
from django.conf import settings
from celery import shared_task
from zibal.client import ZibalIPGClient
from zibal.exceptions import RequestError, ResultError


from product.models import ProductVariant
from order.models import Order


logger = logging.getLogger("order")


@shared_task(bind=True, max_retries=5, default_retry_delay=45)
def process_payment(self, track_id: int, order_id: int) -> None:
    """
    After initializing an IPG payment transaction after 20 minutes, the
    transaction status should be checked and the order should be put into
    the appropriate state based on the response recieved from the IPG
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.exception(
            (
                f"Failed to resolve given order object using order_id: {order_id} "
                f"from the database in the following task: \n"
                f"task ID: {self.task.id} | task name: {self.request.task}"
            )
        )
        return

    if order.status not in (Order.UNPAID, Order.PAYING):
        return

    client = ZibalIPGClient(
        settings.ZIBAL_MERCHANT, raise_on_invalid_result=True, logger=logger
    )
    try:
        response_data = client.inquiry_transaction(track_id=track_id)
        if response_data.status == 2:  # paid but unverified
            verify_data = client.verify_transaction(track_id)
            order.paid_amount = verify_data.amount
            order.status = Order.PROCESSING
        elif response_data.status == 1: # paid and verified
            order.paid_amount = response_data.amount
            order.status = Order.PAID
        else:
            order.status = Order.UNPAID
        order.save()
    except RequestError as exc:
        raise self.retry(exc=exc)
    except ResultError as exc:
        logger.error(
            f"The received result response from IPG is unacceptable: {exc}"
            f"order_id: {order_id} | "
            f"task id: {self.task.id} | task name: {self.request.task}"
        )
    except Order.DoesNotExist:
        logger.error(
            (
                f"Failed to resolve given order object using order_id: {order_id} "
                f"from the database in the following task: \n"
                f"task ID: {self.task.id} | task name: {self.request.task}"
            )
        )


@shared_task(bind=True)
def cancel_unpaid_order(self, order_id):
    """
    For cancelling orders which haven't been paid for about 1-2 hours,
    which will also release the reserved stocks occupied by the order.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.error(
            (
                f"Failed to resolve given order object using order_id: {order_id} "
                f"from the database in the following task: \n"
                f"task ID: {self.task.id} | task name: {self.request.task}"
            )
        )
        return
    if order.status == Order.PAYING:
        raise self.retry(countdown=60 * 20)
    if order.status == Order.UNPAID:
        # release the kraken!
        product_variants = []
        for order_item in order.items.all():
            product_variant = order_item.product_variant
            product_variant.reserved_stock -= order_item.quantity
            product_variant.on_hand_stock += order_item.quantity
            product_variants.append(product_variant)
        order.status = Order.CANCELLED
        with transaction.atomic():
            ProductVariant.objects.bulk_update(
                product_variants, ["reserved_stock", "on_hand_stock"]
            )
            order.save()
