import pytest

from .models import EcomUser

@pytest.mark.django_db
def test_user_create():
    EcomUser.objects.create_user('Mike', '09377964142', 'Mikesbastion@gmail.com', 'MikesPassword')
    assert EcomUser.objects.count() == 1