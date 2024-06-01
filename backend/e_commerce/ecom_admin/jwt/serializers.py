from typing import Any, Dict

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenVerifySerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import Token, RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken

from ecom_admin.models import EcomAdmin
from ecom_core.validators import validate_token_type


class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = EcomAdmin.USERNAME_FIELD

    @classmethod
    def get_token(cls, user: EcomAdmin) -> Token:
        token = super().get_token(user)
        token["user_type"] = "admin"
        return token


class AdminTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs: Dict[str, None]) -> Dict[Any, Any]:
        token = UntypedToken(attrs["token"])
        validate_token_type(token, "admin")
        return super().validate(attrs)


class AdminTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh = RefreshToken(attrs["refresh"])
        validate_token_type(refresh, "admin")
        return super().validate(attrs)
