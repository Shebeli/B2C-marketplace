from typing import Optional

from click import Option
from django.utils.translation import gettext_lazy as _


class ResponseBaseError(Exception):
    """Abstract class used for other custom errors"""

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[int] = None,
        http_status: Optional[int] = None,
        *args,
    ):
        if not self.message or not message:
            raise RuntimeError(
                "A `message` arg should be provided either as a class attribute or as an argument passed to __init__"
            )
        if not self.code or not code:
            raise RuntimeError(
                "A `code` arg should be provided either as a class attribute or as an argument passed to __init__"
            )
        self.message = message or self.message
        self.code = code or self.code
        if not http_status or self.http_status:
            self.http_status = 400
        super().__init__(self.message)

    def as_dict(self):
        return {
            "code": self.code,
            "message": str(self.message),
        }


class ProductUnavailableError(ResponseBaseError):
    "Product has no available stocks."

    code = 1
    message = _("This product is currently unavailable.")


class CartQuantityExceedError(ResponseBaseError):
    "Selected cart item quantity exceeds the items available stocks."

    code = 2
    message = _("The selected quantity exceeds the product's available stocks.")


class OrderOngoingExistsError(ResponseBaseError):
    "A pending order is already on going with the same seller."

    code = 3
    message = _("An order is already going on with the same seller")


class OrderBelowMinError(ResponseBaseError):
    "The orders total amount is lower than the minimum required amount."

    code = 4
    message = _("The order's total amount should be higher than the set minimum amount")


class CartNoItemsError(ResponseBaseError):
    "Used when a cart is empty"

    code = 5
    message = _("The cart doesn't contain any items")


class OrderInvalidAddressError(ResponseBaseError):
    "The address is not valid for the associated order"

    code = 6
    message = _("The given address is invalid or doesn't exist.")


class OrderUpdateBySellerError(ResponseBaseError):
    "Order can be updated by seller to a specific set of statuses."

    code = 7
    message = _(
        "The order can be only updated to one of the following statuses: PROCESSING, SHIPPED or CANCELLED."
    )


class OrderCompletedError(ResponseBaseError):
    "Order is in completed status, and thus the status of the order cannot be modified."

    code = 8
    message = _("The order is already completed, and thus it cannot be modified.")


class CartNotSameSellerError(ResponseBaseError):
    "Cart items should only belong to only one seller"

    code = 9
    message = _("Cart items should belong to only one seller")


class SellerInactiveError(ResponseBaseError):
    "Seller's account is inactive"

    code = 10
    message = _(
        "The request action cannot be performed due to seller's account being invalid."
    )


class CartSameSellerError(ResponseBaseError):
    "Adding items to cart's from user's own seller defined products"

    code = 11
    message = _("Cannot add items from the user's own shop to the cart")


class ProductDisabledError(ResponseBaseError):
    "Product is disabled by the owner"

    code = 12
    message = _("Product is disabled via it's owner")


class OrderIsFinishedError(ResponseBaseError):
    "When an attempt is made to modify an order which is completed (orders should be immutuable when they are finished)"

    code = 13
    message = _("Order is completed and thus it cannot be modified.")


class WalletNotEnoughCurrencyError(ResponseBaseError):
    code = 14
    message = _("Not enough wallet currency to perform the requsted action.")


class ImproperOrderUpdateError(ResponseBaseError):
    "When an order is updated improperly, an error message should be usually passed for better clarity."

    code = 15
    message = _("The requested operation to update or modify the order is invalid.")


class InvalidOrderError(ResponseBaseError):
    "For some reason the order isn't valid due to the order or its related objects not being what expected by the server."

    http_status = 500
    code = 16
    message = _(
        "The requested order or its associated data is not what the server expects. Refer to customer support."
    )