from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from ecom_user.urls import router as user_router

urlpatterns = [
    path("api/user/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("api/user/token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/user/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("api/user/", include((user_router.urls))),
]
