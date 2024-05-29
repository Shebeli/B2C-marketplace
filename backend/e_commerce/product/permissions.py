from rest_framework.permissions import BasePermission, SAFE_METHODS


# object permission checking is intented to be developed in
# the future to check if the admin is eligible to do a requested action or not.
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_admin
            and request.user.is_authenticated
        )
