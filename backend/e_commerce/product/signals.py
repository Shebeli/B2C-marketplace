from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductVariant


@receiver(post_save, sender=ProductVariant)
def assign_main_variant_on_creation(sender, instance, created, **kwargs):
    product = instance.product
    if not product.main_variant:
        instance.product.main_variant = instance
        instance.product.save()


@receiver(post_delete, sender=ProductVariant)
def assign_main_variant_on_deletion(sender, instance, **kwargs):
    product = instance.product
    if product.main_variant == instance:
        new_main_variant = ProductVariant.objects.filter(product=product).first()
        product.main_variant = new_main_variant  # might be null
        product.save()
