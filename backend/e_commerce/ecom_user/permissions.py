from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    "Allows access only to Anonymous users"

    def has_permission(self, request, view):
        return not request.user or request.user.is_anonymous
