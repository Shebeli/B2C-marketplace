from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from product.models import ProductVariant


@receiver(post_save, sender=ProductVariant)
def set_main_variant_on_product_on_save(sender, instance, created, **kwargs):
    product = instance.product
    if not product.main_variant:
        product.main_variant = instance
        product.save()


@receiver(post_delete, sender=ProductVariant)
def set_main_variant_on_product_on_delete(sender, instance, **kwargs):
    product = instance.product
    if not product.main_variant:
        new_variant = product.variants.first()
        product.main_variant = new_variant
        product.save()
