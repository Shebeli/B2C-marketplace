from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    main_image = models.ImageField(blank=True)
    main_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    tags = models.ManyToManyField(Tag, related_name="products")


class TechnicalDetailAttribute(models.Model):
    name = models.CharField(
        max_length=40, verbose_name="technical attribute", db_index=True
    )

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)


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


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    variation = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    stock = models.PositiveIntegerField()
    reserved_stock = models.PositiveIntegerField(default=0)

    @property
    def available_stock(self):
        return self.stock - self.reserved_stock

    def save(self, *args, **kwargs):
        if self.reserved_stock > self.stock:
            raise ValueError("Reserved stock cannot be larger than total stock")
        return super().save(*args, **kwargs)


class ProductVariantImage(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField()
