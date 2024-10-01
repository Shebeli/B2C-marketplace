from django.db import models

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
    all types of financial records, and thus its purpose is only
    for read only operations on the client side.

    Depending on the transaction type, only some fields are required
    to be provided (and so other unrequired fields should be null).
    """

    wallet = models.ForeignKey(
        "Wallet",
        on_delete=models.DO_NOTHING,
        related_name="transactions",
        blank=True,
        null=True,
        help_text="If the wallet is involved in the transaction",
    )
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        help_text="If an order is involved in the transaction",
    )
    payment_track_id = models.IntegerField(
        blank=True,
        null=True,
        help_text="If the transaction's type is deposit",
    )
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="If the transaction's type is order revenue",
    )
    ORDER_REVENUE = "OR"  # user selling items via an order
    ORDER_PAYMENT = "OP"  # user buying items via an order
    WITHDRAWAL = "WD"  # user requesting a withdrawal from their wallet
    DEPOSIT = "PM"  # user depositing money to their wallet via payment
    CANCELLATION = "CC"
    TRANSACTION_TYPES = {
        DEPOSIT: "Deposit",
        WITHDRAWAL: "Withdrawal",
        ORDER_REVENUE: "Order Revenue",
        ORDER_PAYMENT: "Order Payment",
        CANCELLATION: "Cancellation",
    }
    type = models.CharField(choices=TRANSACTION_TYPES)

    class Meta:
        ordering = ["-created_at"]


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

    ORDER = "OD"
    WALLET = "WL"
    PAYMENT_TYPES = {
        ORDER: "Order",
        WALLET: "Wallet",
    }
    type = models.CharField(max_length=2, choices=PAYMENT_TYPES)
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
