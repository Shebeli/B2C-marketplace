import pytest

from ecom_user.models import EcomUser
from ecom_user_profile.models import SellerProfile, CustomerProfile


@pytest.mark.django_db
def test_profiles_are_created_upon_user_creation():
    user = EcomUser.objects.create_user(phone="09377964142")
    assert user.seller_profile and user.customer_profile
