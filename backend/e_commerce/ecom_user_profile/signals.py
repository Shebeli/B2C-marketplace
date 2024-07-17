from django.db.models.signals import post_save
from django.dispatch import receiver
from ecom_user.models import EcomUser
from .models import SellerProfile, CustomerProfile


@receiver(post_save, sender=EcomUser)
def create_profiles(sender, instance, created, **kwargs):
    if created:
        SellerProfile.objects.create(user=instance)
        CustomerProfile.objects.create(user=instance)
