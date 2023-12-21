from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsNotAdminOnlyCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == "POST":
            return True

        elif request.method in permissions.SAFE_METHODS and request.user.is_staff:
            return True

        return False
