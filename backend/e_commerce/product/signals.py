import logging

from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

from .cache_keys import (
    FULLCATEGORIES_CACHE_KEY,
    SUBCATEGORIES_CACHE_KEY,
    breadcrumb_cache_key,
)
from .models import Category, MainCategory, ProductVariant, SubCategory

logger = logging.getLogger("django")


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


@receiver([post_save, post_delete], sender=SubCategory)
def invalidate_subcategory_cache(sender, instance, **kwargs):
    logger.info("Cache invalidated for subcategories.")
    cache.delete(SUBCATEGORIES_CACHE_KEY)
    cache.delete(breadcrumb_cache_key(instance.id))


@receiver([post_save, post_delete], sender=SubCategory)
@receiver([post_save, post_delete], sender=Category)
@receiver([post_save, post_delete], sender=MainCategory)
def invalidate_full_category_cache(sender, instance, **kwargs):
    logger.info(
        f"Cache invalidated for full category by model {sender.__name__} with ID {instance.id}"
    )
    cache.delete(FULLCATEGORIES_CACHE_KEY)
