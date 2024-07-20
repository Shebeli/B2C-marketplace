from rest_framework.permissions import BasePermission, SAFE_METHODS
from ecom_user.models import EcomUser


# object permission checking is intented to be developed in
# the future to check if the admin is eligible to do a requested action or not.
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_admin
            and request.user.is_authenticated
        )


class IsOwner(BasePermission):
    message = "User is not the owner of this object"

    def has_object_permission(self, request, view, obj):
        "Object should have a 'owner' attribute referencing to user instance"
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsSellerVerified(BasePermission):
    message = "User's seller profile isn't verified"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if isinstance(request.user, EcomUser):
            return bool(request.user.seller_profile.is_verified)
        return False
