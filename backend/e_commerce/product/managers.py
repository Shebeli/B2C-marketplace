from django.db import models
from django.db.models import Sum, Case, When


class ProductQuerySet(models.QuerySet):
    def with_available_stock(self):
        return self.annotate(available_stock=Sum("variants__available_stock"))

    def with_total_number_sold(self):
        return self.annotate(total_number_sold=Sum("variants__numbers_sold"))

    def with_main_variant(self):
        if self.main_variant:
            return self.annotate(
                main_price=self.main_variant.price,
                main_image=self.main_variant.image,
            )

    def with_in_stock(self):
        expression = Case(
            When(variants__available_stock__gt=0, then=True),
            default=False,
            output_field=models.BooleanField(),
        )
        return self.annotate(in_stock=expression)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().with_available_stock().filter(available_stock__gt=0)

    def unavailable(self):
        return self.get_queryset().with_available_stock().filter(available_stock=0)
