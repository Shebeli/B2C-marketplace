from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import ProductVariant


@receiver(post_save, sender=ProductVariant)
def assign_main_variant_on_creation(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            product = instance.product
            if not product.main_variant:
                instance.product.main_variant = instance
                instance.product.save(update_fields=["main_variant"])


@receiver(pre_delete, sender=ProductVariant)
def assign_main_variant_on_deletion(sender, instance, **kwargs):
    product = instance.product
    with transaction.atomic():
        if product.main_variant == instance:
            new_main_variant = (
                ProductVariant.objects.filter(product=product)
                .exclude(id=instance.id)
                .first()
            )
            product.main_variant = (
                new_main_variant  # might be null if no other variants exist
            )
            product.save(update_fields=["main_variant"])
