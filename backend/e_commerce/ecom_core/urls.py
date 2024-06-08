from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from ecom_user.urls import router as user_router
from ecom_user_profile.urls import urlpatterns as user_profile_urlpatterns
from ecom_admin.urls import urls as admin_urls


urlpatterns = [
    path(
        "api/user/token/", TokenObtainPairView.as_view(), name="user-token-obtain-pair"
    ),
    path(
        "api/user/token/refresh", TokenRefreshView.as_view(), name="user-token-refresh"
    ),
    path("api/user/token/verify/", TokenVerifyView.as_view(), name="user-token-verify"),
    path("api/user/", include((user_router.urls + user_profile_urlpatterns))),
    path("api/admin/", include(admin_urls)),
]
