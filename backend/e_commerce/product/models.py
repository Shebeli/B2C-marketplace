from django.db import models
from django.core import exceptions
from django.db.models import F, Sum

from ecom_core.validators import validate_rating
from ecom_user.models import EcomUser
from .managers import ProductManager


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
    """
    Since the fields on_hand_stock, reserverd_stock, available_stock and total_number_sold for
    a product is calculated by aggregating the product's variants related fields, for products
    with no variants, a single product variant is created so the whole aggregation calculations for
    mentioned fields are the same with products with more than one variant, thus the aggregation
    calculations are consistent for all products with different number of product variants.
    """

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

    objects = ProductManager()

    def increase_view_count(self) -> None:
        self.view_count = F("view_count") + 1  # to avoid race condition
        self.save(update_fields=["view_count"])
        self.refresh_from_db(fields=["view_count"])

    def get_on_hand_stock(self):
        return self.variants.aggregate(on_hand_stock=Sum(F("on_hand_stock")))[
            "on_hand_stock"
        ]

    def get_reserved_stock(self):
        return self.variants.aggregate(reserved_stock=Sum(F("reserved_stock")))[
            "reserved_stock"
        ]

    def get_available_stock(self):
        return self.variants.aggregate(available_stock=Sum(F("available_stock")))[
            "available_stock"
        ]

    def get_number_sold(self):
        return self.variants.aggregate(number_sold=Sum(F("numbers_sold")))[
            "number_sold"
        ]

    @property
    def tag_names(self):
        return [tag.name for tag in self.tags.all()]


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    on_hand_stock = models.PositiveIntegerField()
    reserved_stock = models.PositiveIntegerField(default=0)
    available_stock = models.GeneratedField(
        expression=F("on_hand_stock") - F("reserved_stock"),
        output_field=models.PositiveIntegerField(),
        db_persist=True,
    )
    numbers_sold = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.reserved_stock > self.on_hand_stock:
            raise exceptions.ValidationError(
                "Reserved stock cannot be larger than on-hand inventory"
            )
        return super().save(*args, **kwargs)

    @property
    def is_available(self):
        return self.available_stock > 0

    @property
    def owner(self):
        return self.product.owner


class ProductVariantImage(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField()


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

    @property
    def owner(self):
        return self.product.owner
