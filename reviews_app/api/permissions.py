from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """
    Permission class to allow access only to authenticated users 
    with type 'customer'.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has type 'customer'.
        
        Returns:
            True if user is authenticated and type is 'customer', else False.
        """
        return bool(request.user and
                    request.user.is_authenticated and
                    getattr(request.user, 'type', None) == 'customer')

class IsReviewOwner(BasePermission):
    """
    Object-level permission to allow only the reviewer (owner) to edit/delete
    a review.
    """
    message = "You are not allowed to edit this review."

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the review.
        
        Args:
            request: HTTP request object
            view: View instance
            obj: Review object being accessed
        
        Returns:
            True if the request user is the reviewer, else False
        """
        return obj.reviewer == request.user or request.user.is_staff
