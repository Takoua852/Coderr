from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and
                    request.user.is_authenticated and
                    getattr(request.user, 'type', None) == 'customer')


class IsBusinessOwner(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return getattr(request.user, 'type', None) == 'business'

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
