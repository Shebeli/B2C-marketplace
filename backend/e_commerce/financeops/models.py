from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ecom_user.models import EcomUser
from ecom_user_profile.models import BankCard
from order.models import Order


class Wallet(models.Model):
    user = models.OneToOneField(
        "ecom_user.EcomUser",
        on_delete=models.DO_NOTHING,
        related_name="wallet",
    )
    balance = models.PositiveBigIntegerField(default=0)


class FinancialRecord(models.Model):
    """
    This model is intended to be used only by server for recording
    all types of financial records.

    Depending on the transaction type, only some fields are required
    to be provided (and so other unrequired fields should be null).
    """

    amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, blank=True)
    wallet = models.ForeignKey(
        "Wallet",
        on_delete=models.DO_NOTHING,
        related_name="transactions",
        blank=True,
        null=True,
        help_text="If the wallet is involved in the transaction",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        help_text="If an order is involved in the transaction",
    )
    payment = models.ForeignKey(
        "Payment",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="If the transaction's type has a payment involved",
    )
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="If the transaction's type is order revenue",
    )
    ORDER_REVENUE = "OR"  # seller's wallet balance increases after 7 days of delivery
    DIRECT_PAYMENT = "OP"  # customer paying an order via direct payment method
    WALLET_PAYMENT = "WP"  # customer paying an order via wallet payment method
    WITHDRAWAL = "WD"  # user requesting a withdrawal from their wallet
    WALLET_REFUND = "RF"  # order getting refunded to user's wallet
    DIRECT_REFUND = "DF"  # order getting refunded using card to card transfer
    DEPOSIT = "PM"  # user increasing their wallet balance via payment
    OTHER = "OT"  # other kind of transaction that doesn't fit to any other category
    CANCELLATION = "CC"
    TRANSACTION_TYPES = {
        DEPOSIT: "Deposit",
        WITHDRAWAL: "Withdrawal",
        ORDER_REVENUE: "Order Revenue",
        DIRECT_PAYMENT: "Order Direct Payment",
        WALLET_PAYMENT: "Order Wallet Payment",
        CANCELLATION: "Cancellation",
    }
    type = models.CharField(choices=TRANSACTION_TYPES, max_length=2)

    class Meta:
        ordering = ["-created_at"]


class Payment(models.Model):
    """
    Used for direct IPG payments, depending on the payment type,
    only one of the fields `order` or `wallet` should be provided.

    Only one instance of payment should exist for each `Order` instance
    or a `Wallet` balance increase operation, which means if an instance
    of `Payment` already exists when a new payment attempt is made, the
    already existing instance will be updated instead.

    Whenever an instance of this model is PAYING, a task should check in x minutes
    to conduct whether the payment was paid or not and update the status to
    CANCELLED if it was not paid.

    Used whenever a payment is involved for either paying an order, or increasing
    the balance of the wallet. The criteria for order and payment is the following:

    - Order: Only one instance of payment exists per order (assuming the order payment
    method is via direct payment).
    - Wallet:


    If an instance of the `Payment` model payment status is PAYING, a celery task
    should check in X minutes and update the payment status by inqurying the payment
    from the provided IPG server.
    """

    paid_by = models.ForeignKey(
        EcomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="payments",
    )
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ZIBAL = "ZB"
    ASAN_PARDAKHT = "AP"
    IPG_CHOICES = {ZIBAL: "Zibal", ASAN_PARDAKHT: "Asan Pardakht"}
    ipg_service = models.CharField(choices=IPG_CHOICES, max_length=2)

    is_used = models.BooleanField(
        default=False,
        help_text=(
            "This field indicates that whether this payment has been checked "
            "to either update an order to PAID status, or to increase "
            "the balance of a wallet."
        ),
    )
    track_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Payment's track id which is provided by the IPG service",
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment",
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    CANCELLED = "CC"
    UNPAID = "UP"
    PAYING = "PY"
    PAID = "PD"
    PAYMENT_STATUSES = {
        CANCELLED: "Cancelled",
        UNPAID: "Unpaid",
        PAYING: "Paying",
        PAID: "Paid",
    }
    status = models.CharField(max_length=2, choices=PAYMENT_STATUSES)

    @property
    def is_payment_link_expired(self) -> bool:
        expire_time = settings.PAYMENT_LINK_EXPIRY_TIME
        if self.track_id_submitted_at > timezone.now() - timedelta(minutes=expire_time):
            return True
        return False

    def get_payment_link(self) -> str | None:
        if not self.is_payment_link_expired:
            return None
        base_url = settings.IPG_SERVICE_BASE_URL[self.service_name]
        return base_url + self.track_id


class WithdrawalRequest(models.Model):
    """For requesting withdrawal from the wallet"""

    PAID = "AP"
    REFUSED = "RF"
    PENDING = "PD"
    REQUEST_STATUSES = {
        PAID: "PAID",
        REFUSED: "Refused",
        PENDING: "Pending",
    }
    status = models.CharField(max_length=2, choices=REQUEST_STATUSES, default=PENDING)
    bank_card = models.ForeignKey(
        BankCard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="withdrawal_requests",
    )
    amount = models.PositiveBigIntegerField()
    refuse_reason = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def requester(self):
        return self.bank_card.user


class MoneyTransferRequest(models.Model):
    """For refunds and other related money transfer requests from the server to users."""

    requested_by = models.ForeignKey(
        EcomUser,
        verbose_name=_("Requesting user"),
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    verified_by = models.ForeignKey(
        "ecom_admin.EcomAdmin",
        verbose_name=_("Verified by admin"),
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    is_verified = models.BooleanField(
        default=False,
        help_text="Indicating whether the money transfer request is valid or not.",
    )
    is_paid = models.BooleanField(default=False)
    tracking_code = models.IntegerField(blank=True)


# class IPG(models.Model):
#     service_name = models.CharField(max_length=50)
#     api_key = models.CharField(max_length=100)
#     api_endpoint = models.URLField()
#     status_check_url = models.URLField()
