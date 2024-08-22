from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .serializers import (
    AdminTokenObtainPairSerializer,
    AdminTokenRefreshSerializer,
    AdminTokenVerifySerializer,
)


class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class AdminTokenVerifyView(TokenVerifyView):
    serializer_class = AdminTokenVerifySerializer

class AdminTokenRefreshView(TokenRefreshView):
    serializer_class = AdminTokenRefreshSerializer