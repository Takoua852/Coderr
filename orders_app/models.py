from django.db import models
from django.conf import settings
from offers_app.models import OfferDetail
from django.utils import timezone


class Order(models.Model):
    """
    Model representing an Order placed by a customer for a specific OfferDetail.

    Attributes:
        customer_user: ForeignKey to the customer who placed the order.
        business_user: ForeignKey to the business fulfilling the order.
        offer_detail: ForeignKey to the associated OfferDetail.
        title: Title of the order, copied from OfferDetail.
        revisions: Number of allowed revisions.
        delivery_time_in_days: Estimated delivery time in days.
        price: Price of the order.
        features: List of features for this order (stored as JSON).
        offer_type: Type of the offer detail (basic, standard, premium).
        status: Current status of the order (in_progress, completed, cancelled).
        created_at: Timestamp when the order was created.
        updated_at: Timestamp when the order was last updated.
    """

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_orders'
    )

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_orders'
    )
   
    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    title = models.CharField(max_length=200)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=50, blank=True, default='basic')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'
    )


    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation of the order.
        """
        return f"Order {self.id} - {self.title} ({self.status})"