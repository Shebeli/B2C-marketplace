from typing import Tuple

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import Token

from ecom_admin.models import EcomAdmin


class EcomAdminBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if (username is None and email is None) or password is None:
            return
        try:
            ecom_admin = EcomAdmin.objects.get(Q(username=username) | Q(email=email))
        except EcomAdmin.DoesNotExist:
            return None
        else:
            if ecom_admin.check_password(password) and self.user_can_authenticate(
                ecom_admin
            ):
                return ecom_admin

    def get_user(self, user_id):
        try:
            return EcomAdmin.objects.get(pk=user_id)
        except EcomAdmin.DoesNotExist:
            return None


class EcomAdminJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = EcomAdmin

    def authenticate(self, request: Request) -> Tuple[EcomAdmin, Token] | None:
        auth_info = super().authenticate(request)
        if not auth_info:
            return None
        token, user = auth_info
        if token.get("user_type") != "admin":
            raise InvalidToken(
                "This token's user type doesn't have the required authorization."
            )
        return user, token
