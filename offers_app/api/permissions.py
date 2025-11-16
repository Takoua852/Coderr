from rest_framework import permissions

class IsBusinessProfileOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return getattr(request.user, 'type', None) == 'business'

class IsOwnerOrReadOnly(permissions.BasePermission):
 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    

