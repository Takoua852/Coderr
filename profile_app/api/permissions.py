from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Custom object-level permission to allow access only to the owner of an object.

    Usage:
        - Can be applied to views where only the creator/owner of the object
          should be able to update or delete it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the object.

        Args:
            request: HTTP request object
            view: View instance
            obj: Object being accessed

        Returns:
            True if the request user is the owner, False otherwise
        """
        return obj.user == request.user 

