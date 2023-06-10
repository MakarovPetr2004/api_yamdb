from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
            )
        )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated and (
                    request.user.is_admin
                )
            )
        )


class AuthorOrModerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role == 'admin' or user.role == 'moderator':
            return True

        author = obj.author
        if author == user:
            return True

        return False
