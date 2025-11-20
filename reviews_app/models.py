from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Model representing a review given by a customer to a business user.

    Attributes:
        business_user: ForeignKey to the business user being reviewed.
        reviewer: ForeignKey to the customer user who wrote the review.
        rating: Integer rating from 1 to 5 (inclusive).
        description: Optional textual description of the review.
        created_at: Timestamp when the review was created.
        updated_at: Timestamp when the review was last updated.
    """
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='written_reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the review.
        """
        return f"Review {self.id} by {self.reviewer} for {self.business_user}"

