from typing import Union

from django.db import models
from django.db.models import F, Sum
from ecom_user.models import EcomUser
from ecom_user_profile.models import CustomerAddress
from product.models import ProductVariant


# Since the business model is a B2C multi vendor platform and the
# web service is not responsible for centralizing the different
# ordered products from different vendors, thus customers CANNOT add
# items to their cart/orders from different shops, and thus required
# validations should be in place for this matter.


class Cart(models.Model):
    user = models.ForeignKey(
        EcomUser, on_delete=models.SET_NULL, null=True, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self) -> Union[int, float]:
        return self.items.aggregate(
            total_price=Sum(F("items__price") * F("items__quantity"))
        )["total_price"]


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=False
    )
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self) -> Union[int, float]:
        return self.product_variant.price * self.quantity


class Order(models.Model):
    """
    Due to business policies, When an order is created, the order cannot be modified
    by the customer with the exception of the order getting cancelled if its only in
    PENDING state.\n
    The order can also be cancelled depending on the seller's policies if it is in
    other states such as PROCESSING or SHIPPED.\n
    It is seller's full responsibilty to fully inform the customer of its order
    policies before the purchase, and its the customer's responsiblity to adhere
    to the seller's declared order policies before accepting the order.
    """

    UNPAID = "UP"
    PENDING = "PD"
    PROCESSING = "PC"
    SHIPPED = "SH"
    DELIVERED = "DL"
    CANCELLED = "CC"
    REFUNDED = "RF"
    STATUS_CHOICES = {
        UNPAID: "UNPAID",
        PENDING: "Pending",
        PROCESSING: "Processing",
        SHIPPED: "Shipped",
        DELIVERED: "Delivered",
        CANCELLED: "Cancelled",
        REFUNDED: "Refunded",
    }
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    user = models.ForeignKey(
        EcomUser, on_delete=models.SET_NULL, null=True, blank=False
    )
    customer_address = models.ForeignKey(
        CustomerAddress, on_delete=models.SET_NULL, blank=False, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=300, blank=True)
    cancellation_reason = models.CharField(max_length=300, blank=True)
    refund_reason = models.CharField(max_length=300, blank=True)

    def get_total_price(self) -> Union[int, float]:
        return self.items.aggregate(
            total_price=Sum(F("items__price") * F("items__quantity"))
        )["total_price"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=False
    )
    quantity = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    def get_total_price(self) -> Union[int, float]:
        return self.product_variant.price * self.quantity

    @property
    def owner(self):
        return self.product_variant.owner
