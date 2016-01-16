from rest_framework import permissions


class IsOwnerOfJob(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny()
        if request.method == "POST":
            return permissions.AllowAny()

        return obj.owner == request.user
