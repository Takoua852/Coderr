from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerUser(BasePermission):
    """
    Custom permission to allow access only to authenticated users
    with the 'customer' type.
    """

    def has_permission(self, request, view):
        """
        Check if the request user is authenticated and is a customer.

        Returns:
            True if the user is authenticated and has type 'customer', else False.
        """
        return bool(request.user and
                    request.user.is_authenticated and
                    getattr(request.user, 'type', None) == 'customer')


class IsBusinessOwner(BasePermission):
    """
    Custom permission to allow business users to perform write operations.

    Read-only requests (GET, HEAD, OPTIONS) are allowed for any user.
    """

    def has_permission(self, request, view):
        """
        Allow safe methods for any user, otherwise check if user is a business.

        Returns:
            True if the user is allowed to perform the action, else False.
        """
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return (
            request.user.is_authenticated and 
            getattr(request.user, "type", None) == "business"
        )

class IsAdminUser(BasePermission):
    """
    Custom permission to allow access only to admin users (staff).
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated and is staff.

        Returns:
            True if the user is a staff member, else False.
        """
        return request.user.is_authenticated and request.user.is_staff
