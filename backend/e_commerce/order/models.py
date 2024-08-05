from typing import Union

from django.db import models
from django.db.models import F, Sum
from ecom_user.models import EcomUser
from ecom_user_profile.models import CustomerAddress
from product.models import ProductVariant


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
    PENDING = "PD"
    PROCESSING = "PC"
    SHIPPED = "SH"
    DELIVERED = "DL"
    CANCELLED = "CC"
    STATUS_CHOICES = {
        PENDING: "Pending",
        PROCESSING: "Processing",
        SHIPPED: "Shipped",
        DELIVERED: "Delivered",
        CANCELLED: "Cancelled",
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
    notes = models.CharField(max_length=200, blank=True)

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
