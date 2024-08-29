from typing import Optional

from rest_framework import serializers
from django.db import transaction
from django.conf import settings
from order.models import Order

from ecom_user_profile.models import (
    Wallet,
    WalletTransaction,
    BankCard,
    WithdrawalRequest,
)
from ecom_user.models import EcomUser


def increase_balance_with_payment(
    wallet: Wallet, amount: int, payment_track_id: Optional[int]
) -> WalletTransaction:
    """
    For increasing the balance of the given wallet via payment. Will also
    create a `WalletTransaction` instance.
    """
    with transaction.atomic():
        wallet_transaction = WalletTransaction.objects.create(
            wallet=wallet,
            type=WalletTransaction.DEPOSIT,
            amount=amount,
            payment_track_id=payment_track_id,
        )
        wallet.balance += amount
        wallet.save()
    return wallet_transaction


def add_order_revenue_to_wallet(
    wallet: Wallet,
    order: Order,
) -> WalletTransaction:
    """
    Assuming the order's status was just changed to `COMPLETED`, which will
    increase the balance of the given `Wallet` instance via the given `Order`
    instance (The commission rate will be also applied to the amount charged).
    Will also create a `WalletTransaction` instance.
    """
    commission_rate = settings.COMMISSION_RATE
    order_total_price = order.get_total_price()
    with transaction.atomic():
        wallet_transaction = WalletTransaction.objects.create(
            wallet=wallet,
            amount=order_total_price,
            type=WalletTransaction.ORDER_REVENUE,
            order=order,
            commission_rate=commission_rate,
        )
        wallet.balance += order_total_price * (100 - commission_rate)
        wallet.save()
    return wallet_transaction


def pay_order_using_wallet(wallet: Wallet, order: Optional[Order]) -> WalletTransaction:
    """
    Pay an order using wallet's currency, update the order's related field
    and create a wallet transaction instance.
    """
    order_total_price = order.get_total_price()
    if wallet.balance < order_total_price:
        raise serializers.ValidationError(
            "Not enough wallet currency for the requested action"
        )
    wallet.balance -= order_total_price
    order.paid_amount = order_total_price
    order.status = Order.PAID
    with transaction.atomic():
        wallet_transaction = WalletTransaction.objects.create(
            wallet=wallet,
            type=WalletTransaction.PAYMENT,
            amount=order.get_total_price(),
            order=order,
        )
        order.save()
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
            "A pending withdrawal already exists for this user. Please update the withdrawal request instead"
        )
    if amount < withdrawal_min:
        raise serializers.ValidationError(
            f"The minimum required balance for requesting a withdrawal is {withdrawal_min} Rials"
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
            "Theres no pending withdrawal request. please request a withdrawal instead"
        )
    if wallet.balance < amount:
        raise serializers.ValidationError(
            "Not enough wallet currency for the requested action"
        )
    # process
    withdrawal.balance = amount
    withdrawal.save()
    return withdrawal


def pay_withdrawal(withdrawal: WithdrawalRequest) -> WalletTransaction:
    """Pay the given withdrawal using card to card money transfer service"""
    pass
