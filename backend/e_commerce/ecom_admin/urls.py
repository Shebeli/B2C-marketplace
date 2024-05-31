from django.urls import path

from ecom_admin.jwt.views import (
    AdminTokenObtainPairView,
    AdminTokenRefreshView,
    AdminTokenVerifyView,
)

urls = [
    path(r"token/", AdminTokenObtainPairView.as_view(), name="admin-token-obtain-pair"),
    path(r"token/refresh/", AdminTokenRefreshView.as_view(), name="admin-token-refresh"),
    path(r"token/verify/", AdminTokenVerifyView.as_view(), name="admin-token-verify"),
]
