from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from .serializers import (
    AdminTokenVerifySerializer,
    AdminTokenObtainPairSerializer,
    AdminTokenRefreshSerializer,
)

class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class AdminTokenVerifyView(TokenVerifyView):
    serializer_class = AdminTokenVerifySerializer

class AdminTokenRefreshView(TokenRefreshView):
    serializer_class = AdminTokenRefreshSerializer