from django.conf import settings
from ecom_user.models import EcomUser
from ecom_user_profile.models import CustomerAddress
from financeops.models import Wallet
from product.models import ProductVariant

from order.exceptions.errors import (
    CartNoItemsError,
    CartNotSameSellerError,
    CartQuantityExceedError,
    CartSameSellerError,
    OrderBelowMinError,
    OrderInvalidAddressError,
    OrderIsFinishedError,
    OrderOngoingExistsError,
    ProductDisabledError,
    ProductUnavailableError,
    SellerInactiveError,
    WalletNotEnoughCurrencyError,
)
from order.models import Cart, CartItem, Order


def validate_user_owns_address(user: EcomUser, address_id: int) -> None:
    customer_address_obj = CustomerAddress.objects.get(id=address_id)
    if customer_address_obj.user != user:
        raise OrderInvalidAddressError()


def validate_cart_not_empty(cart: Cart) -> None:
    if not cart.items.exists():
        raise CartNoItemsError()


def validate_no_on_going_orders(user: EcomUser) -> None:
    on_going_order_statuses = (
        Order.PAYING,
        Order.PAID,
        Order.PROCESSING,
        Order.SHIPPED,
    )
    seller = user.cart.items.first().seller
    if user.orders.filter(seller=seller, status__in=on_going_order_statuses).exists():
        raise OrderOngoingExistsError()


def validate_minimum_order_amount(customer: EcomUser) -> None:
    """Assuming that empty cart validation is run before this validation"""
    seller = customer.cart.items.first().seller
    order_min = seller.seller_profile.minimum_order_amount
    if not order_min:
        order_min = settings.DEFAULT_ORDER_MINIMUM
    if seller.seller_profile.minimum_order_amount > customer.cart.get_total_price():
        raise OrderBelowMinError()


def validate_cart_item_same_seller(
    selected_variant: ProductVariant, cart: Cart
) -> None:
    cart_item = CartItem.objects.filter(cart=cart).first()
    if cart_item:
        if selected_variant.owner != cart_item.product_variant.owner:
            raise CartNotSameSellerError()


def validate_product_is_available(selected_variant: ProductVariant) -> None:
    if not selected_variant.is_available:
        raise ProductUnavailableError()


def validate_product_is_enabled(selected_variant: ProductVariant) -> None:
    if not selected_variant.product.is_enabled:
        raise ProductDisabledError()


def validate_cart_item_quantity(
    selected_variant: ProductVariant, quantity: int
) -> None:
    if quantity > selected_variant.available_stock:
        raise CartQuantityExceedError()


def validate_seller_is_active(selected_variant: ProductVariant) -> None:
    if not selected_variant.owner.is_verified:
        raise SellerInactiveError()


def validate_seller_is_not_current_user(
    selected_variant: ProductVariant, current_user: EcomUser
) -> None:
    if selected_variant.owner != current_user:
        raise CartSameSellerError()


def validate_order_is_not_finished(order: Order) -> None:
    if order.status in [Order.COMPLETED, Order.DELIVERED]:
        raise OrderIsFinishedError()


def validate_wallet_enough_currency(wallet: Wallet, total_amount: int) -> None:
    if wallet.balance < total_amount:
        raise WalletNotEnoughCurrencyError()


def run_order_creation_validations(user: EcomUser, customer_address: int) -> None:
    validate_cart_not_empty(user.cart)
    validate_user_owns_address(user, customer_address)
    validate_no_on_going_orders(user)
    validate_minimum_order_amount(user)


def run_cart_item_creation_validations(
    user: EcomUser, variant: ProductVariant, quantity: int
) -> None:
    validate_cart_item_same_seller(variant, user.cart)
    validate_product_is_available(variant)
    validate_product_is_enabled(variant)
    validate_cart_item_quantity(variant, quantity)
    validate_seller_is_active(variant)
    validate_seller_is_not_current_user(variant, user)


def run_cart_validations(user: EcomUser, item: CartItem) -> None:
    "Just before an order is going to be created, this validation should be called"
    variant = item.product_variant
    validate_product_is_available(variant)
    validate_cart_item_quantity(variant, item.quantity)
    validate_seller_is_active(variant)
    validate_product_is_enabled(variant)
    validate_seller_is_not_current_user(variant, user)
