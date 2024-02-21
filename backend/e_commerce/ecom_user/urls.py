from rest_framework.routers import DefaultRouter

from .views import UserSignupViewSet, UserProfileViewSet, UserForgotPasswordViewSet

router = DefaultRouter()

router.register(r"signup", UserSignupViewSet, basename='user-signup')
router.register(r"profile", UserProfileViewSet, basename='user-profile')
router.register(r"forgot-password", UserForgotPasswordViewSet, basename='user-forgot-password')