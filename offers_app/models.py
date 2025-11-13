from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Offer(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    @property
    def min_price(self):
        min_detail = self.details.aggregate(models.Min('price'))['price__min']
        return min_detail if min_detail is not None else 0

    @property
    def min_delivery_time(self):
        min_time = self.details.aggregate(models.Min('delivery_time_in_days'))[
            'delivery_time_in_days__min']
        return int(min_time) if min_time is not None else 0


class OfferDetail(models.Model):

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
        return f"{self.title} ({self.offer.title})"
