from django.db import models
from django.conf import settings
from django.utils import timezone

class Offer(models.Model):

    """
    Model representing an Offer created by a user.

    Attributes:
        user: ForeignKey to the user who created the offer.
        title: Title of the offer.
        image: Optional image file associated with the offer.
        description: Optional text description of the offer.
        created_at: Timestamp when the offer was created.
        updated_at: Timestamp when the offer was last updated.
    """


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='offers/', blank=True, null=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class OfferDetail(models.Model):
    """
    Model representing a specific detail or package of an Offer.

    Attributes:
        offer: ForeignKey to the parent Offer.
        title: Title of this offer detail.
        revisions: Number of allowed revisions for this detail.
        delivery_time_in_days: Estimated delivery time in days.
        price: Price of this offer detail.
        features: List of features included in this offer detail (stored as JSON).
        offer_type: Type of the offer detail (basic, standard, or premium).
    """

    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=100, blank=True, default='')
    revisions = models.PositiveIntegerField(blank=True, default=0)
    delivery_time_in_days = models.PositiveIntegerField(blank=True, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    features = models.JSONField(blank=True, default=list)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, blank=True, default='basic')

    def __str__(self):
        """
        String representation of the offer detail.
        """
        return f"{self.title} ({self.offer.title})"
