from django.core import exceptions
from django.db import models
from django.db.models import Case, F, Sum, Value, When
from ecom_core.validators import validate_hex_color, validate_rating
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
# ----------------------
# An Example:
# - Books and Stationery
#   - Books and Magazines
#       - Printed books
#       - Foreign and domestic magazines
# ....


class MainCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    main_category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="categories"
    )

    def __str__(self):
        return self.name


class SubCategoryBreadCrumb(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )

    class Meta:
        unique_together = ("name", "category")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class ProductVariant(models.Model):
    """
    At least one ProductVariant instance should exist for every Product,
    even for products with no variants (i.e. products with single variant or no
    variants both have one ProductVariant instance)
    """

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="variants", db_index=True
    )
    name = models.CharField(max_length=200)
    color = models.CharField(
        max_length=6,
        blank=True,
        help_text="Color's Hex code",
        validators=[validate_hex_color],
    )
    price = models.PositiveIntegerField()
    image = models.ImageField(null=True, blank=True)
    on_hand_stock = models.PositiveIntegerField()
    reserved_stock = models.PositiveIntegerField(default=0)
    available_stock = models.GeneratedField(
        expression=F("on_hand_stock") - F("reserved_stock"),
        output_field=models.PositiveIntegerField(),
        db_persist=True,
        db_index=True,
    )
    number_sold = models.PositiveIntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

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

    class Meta:
        order_with_respect_to = "product"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "color"], name="unique_product_color"
            ),
            models.UniqueConstraint(
                fields=["product", "name"], name="unique_variant_name"
            ),
        ]


class Product(models.Model):
    """
    The main_variant field is the representative of the product, so fields such as price,
    image and etc. are derived from the main variant instance when displaying the product
    information on a generic level.
    Also note that at least one product variant should be created for a Product,
    otherwise the product would not be valid to work with.
    """

    owner = models.ForeignKey(
        EcomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="owner",
    )
    main_variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.DO_NOTHING,  # handled by signals
        blank=True,
        null=True,
        related_name="main_variant_of",
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    subcategory = models.ForeignKey(
        SubCategoryBreadCrumb,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
    )
    tags = models.ManyToManyField(Tag, related_name="products")
    view_count = models.PositiveIntegerField(default=0, db_index=True)
    is_valid = models.GeneratedField(
        expression=Case(
            When(main_variant__isnull=True, then=Value(False)),
            When(owner__isnull=True, then=Value(False)),
            default=Value(True),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        db_index=True,
    )
    is_enabled = models.BooleanField(default=True)

    objects = ProductManager()

    def increase_view_count(self) -> None:
        self.view_count = F("view_count") + 1  # to avoid race condition
        self.save(update_fields=["view_count"])
        self.refresh_from_db(fields=["view_count"])

    def _get_stock_field(self, field: str, use_db: bool = True):
        if use_db:
            results = self.variants.aggregate(stock=Sum(F(field)))
            return results["stock"]
        return sum(getattr(variant, field) for variant in self.variants.all())

    def get_on_hand_stock(self, use_db: bool = True):
        return self._get_stock_field("on_hand_stock", use_db)

    def get_reserved_stock(self, use_db: bool = True):
        return self._get_stock_field("reserved_stock", use_db)

    def get_available_stock(self, use_db: bool = True):
        return self._get_stock_field("available_stock", use_db)

    def get_number_sold(self, use_db: bool = True):
        return self._get_stock_field("number_sold", use_db)

    @property
    def tag_names(self):
        return [tag.name for tag in self.tags.all()]


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
