from rest_framework import permissions

class IsBusinessProfileOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only users with a 'business' profile
    to perform write operations (POST, PUT, DELETE).

    Read-only requests (GET, HEAD, OPTIONS) are allowed for any user.
    """

    def has_permission(self, request, view):
        """
        Check if the request has permission to perform the action.

        Args:
            request: The HTTP request.
            view: The view being accessed.

        Returns:
            True if the request is allowed, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return getattr(request.user, 'type', None) == 'business'

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object
    to perform write operations.

    Read-only requests are allowed for any user.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the action on the object.

        Args:
            request: The HTTP request.
            view: The view being accessed.
            obj: The object being accessed.

        Returns:
            True if the request is allowed, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    

