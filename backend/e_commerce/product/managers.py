from django.apps import apps
from django.db import models
from django.db.models import Exists, F, OuterRef, Sum


class ProductQuerySet(models.QuerySet):
    def with_available_stock(self):
        return self.annotate(available_stock=Sum("variants__available_stock"))

    def with_total_number_sold(self):
        return self.annotate(total_number_sold=Sum("variants__number_sold"))

    def with_main_variant_info(self):
        return self.annotate(
            main_price=F("main_variant__price"),
            main_image=F("main_variant__image"),
        )

    def with_in_stock(self):
        ProductVariant = apps.get_model("product", "ProductVariant")
        in_stock_subquery = ProductVariant.objects.filter(
            product=OuterRef("pk"), available_stock__gt=0
        )
        return self.annotate(in_stock=Exists(in_stock_subquery))


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().with_available_stock().filter(available_stock__gt=0)

    def unavailable(self):
        return self.get_queryset().with_available_stock().filter(available_stock=0)
