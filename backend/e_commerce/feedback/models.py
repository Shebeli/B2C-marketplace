from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ecom_user.models import EcomUser
from order.models import Order
from product.models import Product


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(
        EcomUser,
        verbose_name=_("Reviewed by"),
        on_delete=models.CASCADE,
        blank=False,
    )
    rating = models.PositiveSmallIntegerField(
        choices=[
            (1, "1 Star"),
            (2, "2 Star"),
            (3, "3 Star"),
            (4, "4 Star"),
            (5, "5 Star"),
        ]
    )
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = _("ProductReview")
        verbose_name_plural = _("ProductReviews")
        unique_together = (
            "product",
            "reviewed_by",
        )  # ensures only one review exists per product for each customer

    def __str__(self):
        return f"Review by {self.reviewed_by.full_name} on {self.product}"


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(
        EcomUser,
        verbose_name=_("Commented by"),
        on_delete=models.CASCADE,
        blank=False,
    )
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = _("ProductComment")
        verbose_name_plural = _("ProductComments")
        unique_together = ("product", "commented_by")  # only one comment per product

    def __str__(self):
        return f"Review by {self.commented_by.full_name} on {self.product}"
