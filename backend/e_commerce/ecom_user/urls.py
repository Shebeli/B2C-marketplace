from rest_framework.routers import DefaultRouter

from .views import UserSignUpViewSet, UserProfileViewSet, UserForgotPasswordViewSet

router = DefaultRouter()

router.register(r"signup", UserSignUpViewSet, basename='user-signup')
router.register(r"profile", UserProfileViewSet, basename='user-profile')
router.register(r"forgot-password", UserForgotPasswordViewSet, basename='user-forgot-password')