from typing import Any

from ecom_core.validators import validate_token_type
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, Token, UntypedToken

from ecom_admin.models import EcomAdmin


class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = EcomAdmin.USERNAME_FIELD

    @classmethod
    def get_token(cls, user: EcomAdmin) -> Token:
        token = super().get_token(user)
        token["user_type"] = "admin"
        return token


class AdminTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs: dict[str, None]) -> dict[Any, Any]:
        token = UntypedToken(attrs["token"])
        validate_token_type(token, "admin")
        return super().validate(attrs)


class AdminTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        refresh = RefreshToken(attrs["refresh"])
        validate_token_type(refresh, "admin")
        return super().validate(attrs)
