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
    Custom permission to allow access only to authenticated users
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    """
    Custom permission to allow only business users to perform
    write operations (PATCH, PUT).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT'):
            return getattr(request.user, "type", None) == "business"
        return True


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
