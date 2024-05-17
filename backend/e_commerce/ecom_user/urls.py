from rest_framework.routers import DefaultRouter

from .views import UserSignupViewSet, UserProfileViewSet, UserOnetimeAuthViewSet

router = DefaultRouter()

router.register(r"signup", UserSignupViewSet, basename='user-signup')
router.register(r"profile", UserProfileViewSet, basename='user-profile')
router.register(r"onetime-auth", UserOnetimeAuthViewSet, basename='user-onetime-auth')