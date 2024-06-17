from django.db import models
from django.core import exceptions
from django.db.models import F, Sum

from ecom_core.validators import validate_rating
from ecom_user.models import EcomUser


class MainCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    main_category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="categories"
    )


class SubCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    user = models.ForeignKey(
        EcomUser,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="owner",
        blank=False,
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
    main_image = models.ImageField(blank=True)
    main_price = models.PositiveIntegerField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, related_name="products")
    rating = models.DecimalField(
        default=0.0, max_digits=1, decimal_places=1, validators=[validate_rating]
    )
    view_count = models.PositiveIntegerField(default=0)
    # numbers_sold = models.PositiveIntegerField(default=0)

    def increase_view_count(self) -> None:
        self.view_count = F("view_count") + 1
        self.save(update_fields=["view_count"])

    @property
    def available_stock(self):
        return self.variants.aggregate(
            available_stock=Sum(F("stock") - F("reserved_stock"))
        )


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    variation = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    reserved_stock = models.PositiveIntegerField(default=0)
    numbers_sold = models.PositiveIntegerField(
        default=0
    )  # whenever a product is recieved by a customer and 3 days have passed since, this field should be incremented.

    @property
    def available_stock(self):
        return self.stock - self.reserved_stock

    def save(self, *args, **kwargs):
        if self.reserved_stock > self.stock:
            raise exceptions.ValidationError(
                "Reserved stock cannot be larger than stock"
            )
        return super().save(*args, **kwargs)


class TechnicalDetailAttribute(models.Model):
    name = models.CharField(
        max_length=40, verbose_name="technical attribute", db_index=True
    )


class TechnicalDetail(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="technical_details"
    )
    attribute = models.ForeignKey(
        TechnicalDetailAttribute,
        on_delete=models.CASCADE,
        related_name="technical_details",
    )
    value = models.CharField(
        max_length=50, verbose_name="technical attribute description"
    )

    class Meta:
        unique_together = ("product", "attribute")


class ProductVariantImage(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField()
