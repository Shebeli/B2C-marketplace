from django.dispatch.dispatcher import Signal
from django.dispatch.dispatcher import receiver

from order.models import Cart
from ecom_user.models import EcomUser
from django.db.models.signals import post_save


@receiver(post_save, sender=EcomUser)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
