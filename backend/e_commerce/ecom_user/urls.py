from rest_framework.routers import DefaultRouter

from .views import UserAccountViewSet, UserLoginViewSet

router = DefaultRouter()

router.register(r"login", UserLoginViewSet, basename="user-login")
router.register(r"account", UserAccountViewSet, basename="user-account")
# router.register(r"onetime-auth", UserOnetimeAuthViewSet, basename='user-onetime-auth')
