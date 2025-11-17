from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from reviews_app.models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from .permissions import IsCustomerUser, IsReviewOwner
from rest_framework.filters import SearchFilter, OrderingFilter


class ReviewListCreateView(generics.ListCreateAPIView):

    queryset = Review.objects.all()
    search_fields = ['description']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']
    pagination_class = None
    filter_backends = [SearchFilter, OrderingFilter]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        business_user_id = self.request.query_params.get('business_user_id')
        reviewer_id = self.request.query_params.get('reviewer_id')

        if business_user_id is not None:
            queryset = queryset.filter(business_user__id=business_user_id)

        if reviewer_id is not None:
            queryset = queryset.filter(reviewer__id=reviewer_id)

        return queryset


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()

    def get_permissions(self):
        if self.request.method in ["PATCH", "PUT", "DELETE"]:
            return [IsAuthenticated(), IsReviewOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return ReviewUpdateSerializer
        return ReviewSerializer