from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenVerifySerializer,
    TokenRefreshSerializer,
)
from ecom_admin.models import EcomAdmin

class AdminTokenObtainPainSerializer(TokenObtainPairSerializer):
    