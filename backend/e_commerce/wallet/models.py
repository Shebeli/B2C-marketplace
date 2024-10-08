from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.utils import timezone


from ecom_user_profile.models import BankCard
from ecom_user.models import EcomUser
from order.models import Order


class Wallet(models.Model):
    user = models.OneToOneField(
        "ecom_user.EcomUser",
        on_delete=models.DO_NOTHING,
        related_name="wallet",
    )
    balance = models.PositiveBigIntegerField(default=0)


class Transaction(models.Model):
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
    type = models.CharField(choices=TRANSACTION_TYPES)

    class Meta:
        ordering = ["-created_at"]


class Payment(models.Model):
    """
    Depending on the payment type, only one of the fields `order` or `wallet`
    should be provided.
    """

    user = models.ForeignKey(
        EcomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="payments",
    )
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service_name = models.CharField(max_length=15)
    is_used = models.BooleanField(
        default=False,
        help_text=(
            "This field indicates that whether this payment has been checked "
            "to either update an order to PAID status, or to increase "
            "the balance of a wallet."
        ),
    )
    track_id = models.CharField(max_length=50)
    track_id_time = models.DateTimeField(
        help_text="When `track_id` field is provided/updated, this field should be set to its time"
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

    def is_payment_link_expired(self) -> bool:
        expire_time = settings.PAYMENT_LINK_EXPIRY_TIME
        if self.track_id_time > timezone.now() - timedelta(minutes=expire_time):
            return True
        return False


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
    """For refunds and other related money transfer requests."""

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
    amount = models.BigIntegerField()
    is_verified = models.BooleanField(default=False)
    is_paid = models.BooleanField()
