from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ecom_user.models import EcomUser
from order.models import Order
from product.models import Product


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(
        EcomUser,
        verbose_name=_("Reviewed by"),
        on_delete=models.CASCADE,
        blank=False,
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating should be an integer from 1 to 5",
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("ProductComment")
        verbose_name_plural = _("ProductComments")
        unique_together = ("product", "commented_by")  # only one comment per product

    def __str__(self):
        return f"Review by {self.commented_by.full_name} on {self.product}"
