from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
            or obj.author == request.user
        )

    def has_permission(self, request):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_staff)

