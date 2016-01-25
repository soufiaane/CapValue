from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, account):
        if request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        if request.method == 'POST':
            return (permissions.AllowAny(),)
        if request.user:
            return account == request.user
        return False
