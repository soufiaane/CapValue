from rest_framework import permissions


class IsOwnerOfProxy(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return True
        return obj.owner == request.user
