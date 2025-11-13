from rest_framework import permissions

class IsBusinessProfileOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(request.user, 'type', None) == 'business'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(request.user, 'type', None) == 'business' and obj.user == request.user


        return request.user.type == 'business' and obj.user == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Nur der Ersteller (Owner) darf bearbeiten. GET bleibt für alle erlaubt (oder nur Authenticated).
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Nur Owner darf ändern
        return obj.user == request.user