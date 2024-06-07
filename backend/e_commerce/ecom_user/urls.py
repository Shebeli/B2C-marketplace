from rest_framework.routers import DefaultRouter

from .views import UserSignupViewSet, UserAccountViewSet, UserOnetimeAuthViewSet

router = DefaultRouter()

router.register(r"signup", UserSignupViewSet, basename='user-signup')
router.register(r"account", UserAccountViewSet, basename='user-account')
router.register(r"onetime-auth", UserOnetimeAuthViewSet, basename='user-onetime-auth')