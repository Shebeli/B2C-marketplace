from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from django.conf import settings


class UsernameOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, phone=None, password=None, **kwargs):
        if (username is None and phone is None) or password is None:
            return
        UserModel = get_user_model()
        try:  # phone and username are unique fields and one of them can be null but not both.
            user = UserModel.objects.get(Q(username=username) | Q(phone=phone))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
