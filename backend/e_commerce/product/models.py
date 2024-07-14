from django.db import models
from django.core import exceptions
from django.db.models import F, Sum

from ecom_core.validators import validate_rating
from ecom_user.models import EcomUser


# Overall visualization of different category models is shown in the following tree:
# - MainCategory 1
#   - Category 1
#       - SubCategory 1
#       - SubCategory 2
#       - ...
#       - SubCategory p
#   - ...
#   - Category m
# - ...
# - MainCategory n
# An Example:
# - Books and Stationery
#   - Books and Magazines
#       - Printed books
#       - Foreign and domestic magazines
# ....


class MainCategory(models.Model):  # e.g Digital Product, Books and Stationery
    name = models.CharField(max_length=30, unique=True)


class Category(models.Model):  #
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
    owner = models.ForeignKey(
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

    def increase_view_count(self) -> None:
        self.view_count = F("view_count") + 1  # to avoid race condition
        self.save(update_fields=["view_count"])
        # self.refresh_from_db(fields=['view_count'])

    @property
    def available_stock(self):
        return self.variants.aggregate(available_stock=Sum(F("available_stock")))[
            "available_stock"
        ]

    @property
    def total_number_sold(self):
        return self.variants.aggregate(total_number_sold=Sum(F("numbers_sold")))[
            "total_number_sold"
        ]

    @property
    def tag_names(self):
        return [tag.name for tag in self.tags]


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    reserved_stock = models.PositiveIntegerField(default=0)
    available_stock = models.GeneratedField(
        expression=F("stock") - F("reserved_stock"),
        output_field=models.PositiveIntegerField(),
        db_persist=True,
    )
    numbers_sold = models.PositiveIntegerField(
        default=0
    )  # whenever a product is recieved by a customer and n days have passed since, this field should be incremented.

    def save(self, *args, **kwargs):
        if self.reserved_stock > self.stock:
            raise exceptions.ValidationError(
                "Reserved stock cannot be larger than stock"
            )
        return super().save(*args, **kwargs)


class TechnicalDetail(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="technical_details"
    )
    attribute = models.CharField(max_length=30)
    value = models.CharField(
        max_length=80, verbose_name="technical attribute description"
    )

    class Meta:
        unique_together = ("product", "attribute")


class ProductVariantImage(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField()
