
from django.utils import timezone
from financeops.models import (
    IPGChoice,
    Payment,
    Wallet,
)

from order.models import Order
from order.payment.factory import PaymentGatewayFactory
from order.tasks import cancel_payment


class PaymentService:
    @staticmethod
    def create_payment_for_order(order: Order, selected_ipg: IPGChoice) -> str:
        """
        Creates a payment record and initiates a transaction with the requested IPG.

        Raises:
            PaymentNotImplementedError: Selected IPG is recognized but the client isn't implemented.
            PaymentGatewayNotFoundError: Selected IPG is not recognized.
            PaymentRequestError: Request to IPG has failed (timeouts, network errors and etc.)
            PaymentResponseError: A bad/unexpected response was received from IPG.
        """

        client = PaymentGatewayFactory.get_client(selected_ipg)
        order_total_price = order.get_total_price()
        callback_url = client.get_callback_url()
        response = client.request_transaction(order_total_price, callback_url)

        payment = order.payment or Payment(order=order)
        payment.amount = order_total_price
        payment.track_id = response.track_id
        payment.track_id_submitted_at = timezone.now()
        payment.status = Payment.PAYING
        payment.ipg_service = selected_ipg
        payment.save()
        cancel_payment.apply_async(payment.id, countdown=60 * 15)

        return client.get_payment_link()

    @staticmethod
    def create_payment_for_wallet(
        wallet: Wallet, charge_amount: int, selected_ipg: IPGChoice
    ) -> str:
        client = PaymentGatewayFactory.get_client()
        callback_url = client.get_callback_url()
        response = client.request_transaction(charge_amount, callback_url)

        payment = Payment.objects.create(
            wallet=wallet,
            amount=charge_amount,
            track_id=response.track_id,
            track_id_submitted_at=timezone.now(),
            status=Payment.PAYING,
            ipg_service=selected_ipg,
        )
        cancel_payment.apply_async(payment.id, countdown=60 * 15)

        return client.get_payment_link()
