from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and
                    request.user.is_authenticated and
                    getattr(request.user, 'type', None) == 'customer')
    

class IsReviewOwner(BasePermission):

    message = "You are not allowed to edit this review."
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
