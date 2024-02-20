import pytest 
from rest_framework.test import APIClient


@pytest.fixture
def user_password():
    return '$tR0nG165P@sS\|/oRd09_'

@pytest.fixture
def generate_user(db, django_user_model, user_password):
    def make_user(**kwargs):
        if not kwargs['phone']:
            kwargs['phone'] = '09377964148'
        if not kwargs['username']:
            kwargs['username'] = 'some_test_username'
        kwargs['password'] = user_password
        return django_user_model.objects.create_user(**kwargs)
    return make_user

