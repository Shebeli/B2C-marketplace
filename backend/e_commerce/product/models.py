from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    technical_detail = models.CharField(max_length=200)
    image = models.ImageField()
    price = models.DecimalField(max_digits=20, decimal_places=2)


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    variation = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.PositiveIntegerField()
    reserved_stock = (
        models.PositiveIntegerField()
    )  # stock and reserved_stock are independent of each other.

    @property
    def available_stock(self):
        return self.stock - self.reserved_stock

    def save(self, *args, **kwargs):
        if self.reserved_stock > self.stock:
            raise ValueError("Reserved stock cannot be larger than total stock")
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product_variation = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField()


class Category(models.Model):
    product = models.ManyToManyField(
        Product, related_name="categories", db_table="ProductCategory"
    )
    name = models.CharField(max_length=30)


class Tag(models.Model):
    product = models.ManyToManyField(
        Product, related_name="tags", db_table="ProductTag"
    )
    name = models.CharField(max_length=30)
