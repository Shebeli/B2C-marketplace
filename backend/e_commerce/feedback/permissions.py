from rest_framework.permissions import BasePermission


class IsEcomAdmin(BasePermission):
    """
    Allows access for all types of admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin


class IsCommentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.commented_by == request.user


class IsReviewOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reviewed_by == request.user
