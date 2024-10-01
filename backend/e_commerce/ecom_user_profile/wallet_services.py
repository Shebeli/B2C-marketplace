from typing import Optional

from rest_framework import serializers
from django.db import transaction
from django.conf import settings
from order.models import Order

from ecom_user_profile.models import (
    Wallet,
    Transaction,
    BankCard,
    WithdrawalRequest,
)
from ecom_user
from ecom_user.models import EcomUser

from zibal.client import ZibalIPGClient


def add_order_revenue_to_wallet(
    wallet: Wallet,
    order: Order,
) -> Transaction:
    """
    Assuming the order's status was just changed to `COMPLETED`, which will
    increase the balance of the given `Wallet` instance via the given `Order`
    instance (The commission rate will be also applied to the amount charged).
    Will also create a `WalletTransaction` instance.
    """
    commission_rate = settings.COMMISSION_RATE
    order_total_price = order.get_total_price()
    with transaction.atomic():
        wallet_transaction = Transaction.objects.create(
            wallet=wallet,
            amount=order_total_price,
            type=Transaction.ORDER_REVENUE,
            order=order,
            commission_rate=commission_rate,
        )
        wallet.balance += order_total_price * (100 - commission_rate)
        wallet.save()
    return wallet_transaction


def request_withdrawal(selected_bank_card: BankCard, amount: int) -> WithdrawalRequest:
    """
    Submit a request for withdrawl from the wallet, which result in
    creating a WithdrawalRequest instance.
    """
    wallet = selected_bank_card.user.wallet
    withdrawal_min = settings.WITHDRAWAL_MIN_AMOUNT
    if WithdrawalRequest.objects.filter(
        bank_card__in=selected_bank_card.user.bank_cards,
        status=WithdrawalRequest.PENDING,
    ).exists():
        raise serializers.ValidationError(
            "A pending withdrawal already exists for this user."
            " Please update the withdrawal request instead"
        )
    if amount < withdrawal_min:
        raise serializers.ValidationError(
            "The minimum required balance for requesting a withdrawal"
            f" is {withdrawal_min} Rials."
        )
    if wallet.balance < amount:
        raise serializers.ValidationError(
            "Not enough wallet currency for the requested action"
        )
    return WithdrawalRequest.objects.create(bank_card=selected_bank_card, amount=amount)


def update_withdrawal_request(user: EcomUser, amount: int) -> WithdrawalRequest:
    wallet = user.wallet
    withdrawal = WithdrawalRequest.objects.filter(
        bank_card__in=user.bank_cards, status=WithdrawalRequest.PENDING
    ).first()
    # validations
    if not withdrawal:
        raise serializers.ValidationError(
            "Theres no pending withdrawal request."
            " Please request a new withdrawal instead"
        )
    if wallet.balance < amount:
        raise serializers.ValidationError(
            "Not enough wallet currency for the requested action"
        )
    # process
    withdrawal.balance = amount
    withdrawal.save()
    return withdrawal


def pay_withdrawal(withdrawal: WithdrawalRequest) -> Transaction:
    """Pay the given withdrawal using card to card money transfer service"""
    pass
