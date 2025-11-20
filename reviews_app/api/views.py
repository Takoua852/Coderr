from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from reviews_app.models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from .permissions import IsCustomerUser, IsReviewOwner
from rest_framework.filters import SearchFilter, OrderingFilter


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all reviews or creating a new review.

    Features:
    - GET: List reviews (any authenticated user)
        Optional query params:
            - business_user_id: filter reviews for a specific business
            - reviewer_id: filter reviews by a specific reviewer
    - POST: Create a new review (only authenticated customers)
    - Supports searching by 'description' and ordering by 'updated_at' or 'rating'
    """
    queryset = Review.objects.all()
    search_fields = ['description']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']
    filter_backends = [SearchFilter, OrderingFilter]

    def get_permissions(self):
        """
        Return different permissions based on HTTP method:
        - POST: Only authenticated users with type 'customer' can create
        - GET: Any authenticated user can view
        """
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """
        Return serializer class based on HTTP method:
        - POST: Use ReviewCreateSerializer for creating reviews
        - GET: Use ReviewSerializer for listing reviews
        """
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_queryset(self):
        """
        Optionally filter queryset based on query parameters:
        - business_user_id: filter by business being reviewed
        - reviewer_id: filter by reviewer
        """
        queryset = super().get_queryset()

        business_user_id = self.request.query_params.get('business_user_id')
        reviewer_id = self.request.query_params.get('reviewer_id')

        if business_user_id is not None:
            queryset = queryset.filter(business_user__id=business_user_id)

        if reviewer_id is not None:
            queryset = queryset.filter(reviewer__id=reviewer_id)

        return queryset

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific Review.

    Features:
    - GET: Retrieve review details (any authenticated user)
    - PATCH/PUT: Update review (only the owner can update)
    - DELETE: Delete review (only the owner can delete)
    """
    queryset = Review.objects.all()

    def get_permissions(self):
        """
        Return permissions based on HTTP method:
        - PATCH/PUT/DELETE: Only authenticated users who are the owner of the review
        - GET: Any authenticated user
        """
        if self.request.method in ["PATCH", "PUT", "DELETE"]:
            return [IsAuthenticated(), IsReviewOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """
        Return serializer class based on HTTP method:
        - PATCH/PUT: Use ReviewUpdateSerializer for updates
        - GET/DELETE: Use ReviewSerializer
        """
        if self.request.method in ["PATCH", "PUT"]:
            return ReviewUpdateSerializer
        return ReviewSerializer