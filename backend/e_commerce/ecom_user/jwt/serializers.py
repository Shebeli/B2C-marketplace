from typing import Any, Dict

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.tokens import Token, RefreshToken, UntypedToken, AuthUser

from ecom_core.validators import validate_token_type


class EcomUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token["user_type"] = "normal"
        return token


class EcomUserTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh = self.token_class(attrs["refresh"])
        validate_token_type(refresh, "normal")
        return super().validate(attrs)


class EcomUserTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs: Dict[str, None]) -> Dict[Any, Any]:
        token = UntypedToken(attrs["token"])
        validate_token_type(token, "normal")
        return super().validate(attrs)
