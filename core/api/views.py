from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from reviews_app.models import Review
from auth_app.models import CustomUser
from offers_app.models import Offer
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import status


class BaseInfoView(APIView):
    """
    API endpoint to retrieve general/base information about the platform.

    Returns:
        - review_count: Total number of reviews.
        - average_rating: Average rating of all reviews (rounded to 1 decimal).
        - business_profile_count: Total number of business users.
        - offer_count: Total number of offers.

    Permissions:
        - AllowAny: Accessible by any user (authenticated or not).
    """
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Handles GET requests to fetch the base information.
        """
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg=Avg('rating'))[
            'avg'] or 0
        business_profile_count = CustomUser.objects.filter(type = 'business').count()
        offer_count = Offer.objects.count()

        return Response({
            "review_count": review_count,
            "average_rating": round(average_rating, 1),
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }, status=status.HTTP_200_OK)
