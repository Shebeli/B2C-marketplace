"""
URL configuration for e_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from ecom_user.urls import router as ecom_user_router

urlpatterns = [
    path("api/user/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("api/user/token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/user/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("api/user/", include((ecom_user_router.urls))),
]
