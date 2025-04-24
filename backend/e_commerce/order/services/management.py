import logging

from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ecom_core import settings
from ecom_user.models import EcomUser
from financeops.models import (
    FinancialRecord,
    IPGChoice,
    MoneyTransferRequest,
    Payment,
    Wallet,
)
from product.models import ProductVariant
from zibal.client import ZibalIPGClient
from zibal.exceptions import RequestError

from order.exceptions.errors import (
    ImproperOrderUpdateError,
    InvalidOrderError,
    ResponseBaseError,
)
from order.models import Cart, CartItem, Order, OrderItem
from order.payment.exceptions import PaymentRequestError
from order.payment.factory import PaymentGatewayFactory
from order.services.schemas import OrderCreationSchema
from order.services.validators import (
    run_cart_item_creation_validations,
    run_cart_validations,
    run_order_creation_validations,
    validate_cart_item_quantity,
    validate_product_is_available,
    validate_wallet_enough_currency,
)


class OrderService:
    @staticmethod
    def create_order(data: OrderCreationSchema) -> Order:
        """
        When a new order needs to be created based off on user's current cart,
        the following steps will be executed in order when calling this function:

        1. Create an unsaved instance of `Order`.
        2. Using the `Cart` object from passed in `validated_data`, validate each `CartItem` instance having
        a valid quantity.
        3. For each `CartItem`, create an unsaved `OrderItem` instance using the `Order`
        instance created in step 1.
        4. For each `CartItem`, update its associated `ProductVariant` `reserved_stocks` and
        `on_hand_stock` fields.
        5. Delete user's current cart items.

        The key `order` in passed in arg `validated_data` should be an instance of order
        which hasn't been saved to the database, yet.
        """
        user = data.user

        run_order_creation_validations(user, data.customer_address)
        order = Order(
            status=Order.UNPAID,
            customer=user,
            customer_address=data.customer_address,
            customer_notes=data.notes,
        )

        cart_items = user.cart.items.select_related("product_variant").all()
        variant_ids = [item.product_variant.id for item in cart_items]
        variants = {
            pv.id: pv
            for pv in ProductVariant.objects.select_for_update().filter(
                id__in=variant_ids
            )
        }

        product_variants = []
        order_items = []
        with transaction.atomic():
            for item in cart_items:
                product_variant = variants[item.product_variant.id]
                validate_product_is_available(product_variant)
                validate_cart_item_quantity(item)

                # create order python instances and update the stocks
                order_item = OrderItem(
                    order=order,
                    product_variant=product_variant,
                    submitted_price=product_variant.price,
                    quantity=item.quantity,
                )
                product_variant.reserved_stock += item.quantity
                product_variant.on_hand_stock -= item.quantity

                order_items.append(order_item)
                product_variants.append(product_variant)

            # db operations
            order.save()
            ProductVariant.objects.bulk_update(product_variants, ["reserved_stock"])
            OrderItem.objects.bulk_create(order_items)
            user.cart.items.all().delete()

        return order

    @staticmethod
    def pay_order_using_wallet(wallet: Wallet, order: Order) -> FinancialRecord:
        """
        Pay an order using wallet's currency, update the order's related field
        and create a `FinancialRecord` instance.
        """
        order_total_price = order.get_total_price()
        validate_wallet_enough_currency(wallet, order_total_price)

        with transaction.atomic():
            order.status = Order.PAID
            wallet.balance -= order_total_price
            record = FinancialRecord.objects.create(
                wallet=wallet,
                type=FinancialRecord.WALLET_PAYMENT,
                amount=order.get_total_price(),
                order=order,
            )
            order.save()
            wallet.save()
        return record

    @staticmethod
    def update_order_to_shipped(order: Order, tracking_code: str) -> Order:
        """
        Updates the order's status to SHIPPED with the following changes:
        The order's items stocks will be updated accordingly, and the
        order's tracking code will either be set and the order's status
        will also be updated to SHIPPED.

        If the order's status is already SHIPPED, only the order's
        tracking code will be updated.
        """
        if order.status not in (Order.PAID, Order.SHIPPED, Order.PROCESSING):
            raise ImproperOrderUpdateError(
                "SHIPPED status update is only usable when the order is in PAID"
                ", SHIPPED or PROCESSING state."
            )

        if not tracking_code:
            raise ImproperOrderUpdateError(
                "A tracking code should be provided when updating the status to"
                " shipped or updating the tracking code"
            )

        # if the order is already updated to SHIPPED status, then the assumption is
        # that the current call is intended for updating the order's tracking code.
        if order.status == Order.SHIPPED:
            order.tracking_code = tracking_code
            order.save()
            return order

        order_items = (
            order.items.select_related("product_variant")
            .select_for_update(of=("product_variant",))
            .all()
        )
        with transaction.atomic():
            for item in order_items:
                item.product_variant.reserved_stock -= item.quantity
                item.product_variant.on_hand_stock -= item.quantity
            order.status = Order.SHIPPED
            order.tracking_code = tracking_code
            ProductVariant.objects.bulk_update(
                [item.variant for item in order_items],
                ["reserved_stock", "on_hand_stock"],
            )
            order.save()
        return order

    @staticmethod
    def cancel_order_by_seller(order: Order, cancel_reason: str) -> FinancialRecord:
        """
        Only usable for order instances where the status of the order is
        either PAID or PROCESSING.

        The refund method is based on whether the order was paid using
        wallet or direct payment:
        - If the payment method was direct payment, then a `MoneyTransferRequest`
        instance will also be created, which customer support should handle the
        refund using this instance.
        - If the payment method was wallet payment, then the paid amount will
        be refunded back to the wallet.
        """
        if not cancel_reason:
            raise ImproperOrderUpdateError(
                "A cancellation reason should be provided when cancelling the order."
            )

        # if the following case is true then its assumed that
        # the intention was to update the cancellation reason.
        if order.status == Order.CANCELLED:
            order.cancel_reason = cancel_reason
            order.save()
            return order

        if order.status not in (Order.PAID, Order.PROCESSING):
            raise ImproperOrderUpdateError(
                "Order cannot be cancelled if it is not in PAID or PROCESSING state."
            )

        order_items = (
            order.items.select_related("product_variant")
            .select_for_update(of=("product_variant",))
            .all()
        )
        for item in order_items:
            item.product_variant.reserved_stock -= item.quantity
            item.product_variant.on_hand_stock += item.quantity
        order.status = Order.CANCELLED
        order.cancel_reason = cancel_reason
        order.cancelled_by = Order.SELLER

        record = FinancialRecord.objects.filter(
            order=order,
            type__in=[FinancialRecord.DIRECT_PAYMENT, FinancialRecord.WALLET_PAYMENT],
        ).first()
        if not record:
            raise InvalidOrderError(
                _(
                    "No associated transaction was found for this order. "
                    "Please open a support ticket with order ID included."
                )
            )

        with transaction.atomic():
            if record.type == FinancialRecord.WALLET_PAYMENT:
                customer_wallet = order.customer.wallet
                order_total_price = order.get_total_price()
                customer_wallet.balance += order_total_price
                refund_record = FinancialRecord.objects.create(
                    type=FinancialRecord.WALLET_REFUND,
                    amount=order_total_price,
                    wallet=record.wallet,
                    order=record.order,
                )
            elif record.type == FinancialRecord.DIRECT_PAYMENT:
                MoneyTransferRequest.objects.create(
                    requested_by=order.customer,
                    amount=order.amount,
                )
                refund_record = FinancialRecord.objects.create(
                    type=FinancialRecord.DIRECT_REFUND,
                    amount=order_total_price,
                    order=record.order,
                )
            else:
                raise InvalidOrderError(
                    _(
                        "The associated transaction for the given order is invalid, "
                        "Please open a support ticket with order ID included."
                    )
                )
            ProductVariant.objects.bulk_update(
                [item.product_variant for item in order_items],
                ["reserved_stock", "on_hand_stock"],
            )
            order.save()
            customer_wallet.save()
        return refund_record


class CartService:
    @staticmethod
    def add_item_to_cart(user: EcomUser, variant_id: int, quantity: int) -> Cart:
        product_variant = ProductVariant.objects.get(id=variant_id)
        run_cart_item_creation_validations(product_variant, user, quantity)

        return CartItem.objects.create(
            cart=user.cart,
            product_variant=variant_id,
            quantity=quantity,
        )

    @staticmethod
    def get_user_cart_errors(user: EcomUser) -> dict[int, str]:
        errors = {}
        for item in user.cart.items.all():
            item_errors = []
            try:
                run_cart_validations(item.product_variant)
            except ResponseBaseError as exc:
                item_errors.append(exc.message)
            errors[item.variant.id] = item_errors
        return errors


logger = logging.getLogger("order")


class PaymentService:
    """Provides the following services:
    1. request_payment_for_order
    3. request_payment_for_wallet
    2. verify_payment
    """

    @staticmethod
    def create_payment_for_order(order: Order, selected_ipg: IPGChoice) -> str:
        order_total_price = order.get_total_price()

        client = PaymentGatewayFactory.get_client(selected_ipg)
        try:
            response = client.request_transaction(
            order_total_price, client.get_callback_url()
            )

        payment = order.payment or Payment(order=order)
        payment.amount = order_total_price
        payment.track_id = response.track_id
        payment.track_id_submitted_at = timezone.now()
        payment.status = Payment.PAYING
        payment.ipg_service = selected_ipg
        payment.save()

        return client.get_payment_link()

    @staticmethod
    def create_payment_for_wallet_charge(
        wallet: Wallet, selected_ipg: IPGChoice, amount: int
    ) -> str:
        client = PaymentGatewayFactory.get_client(selected_ipg)
        response = client.request_transaction(amount, client.get_callback_url())

        Payment.objects.create(
            wallet=wallet,
            amount=amount,
            track_id=response.track_id,
            track_id_submitted_at=timezone.now(),
            status=Payment.PAYING,
            ipg_service=selected_ipg,
        )

        return client.get_payment_link()
