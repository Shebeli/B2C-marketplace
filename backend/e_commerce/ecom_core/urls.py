from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from ecom_user.urls import router as user_router
from ecom_user_profile.urls import urlpatterns as user_profile_urlpatterns
from ecom_admin.urls import urls as admin_urls
from product.urls import urlpatterns as product_urls
from order.urls import urlpatterns as order_urls

urlpatterns = [
    # JWT authentication
    path(
        "api/user/token/", TokenObtainPairView.as_view(), name="user-token-obtain-pair"
    ),
    path(
        "api/user/token/refresh", TokenRefreshView.as_view(), name="user-token-refresh"
    ),
    path("api/user/token/verify/", TokenVerifyView.as_view(), name="user-token-verify"),
    # Project apps
    path("api/user/", include((user_router.urls + user_profile_urlpatterns))),
    path("api/admin/", include(admin_urls)),
    path("api/products/", include(product_urls)),
    path("api/order/", include(order_urls)),
    # drf-spectacular, for OpenAPI schema generation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
