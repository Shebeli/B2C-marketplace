from typing import Tuple
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import InvalidToken


class EcomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, phone=None, password=None, **kwargs):
        if (username is None and phone is None) or password is None:
            return
        UserModel = get_user_model()
        try:  # phone and username are unique fields and only one of them is required.
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


class EcomUserJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Tuple[AuthUser, Token] | None:
        auth_info = super().authenticate(request)
        if not auth_info:
            return None
        user, token = auth_info  
        if token.get("user_type") != "normal":
            raise InvalidToken(
                "This token user's type doesn't have the required authorization"
            )
        return user, token
