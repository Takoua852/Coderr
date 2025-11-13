from django.db import models
from django.contrib.auth.models import AbstractUser

    
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    REQUIRED_FIELDS = ['email', 'type']

    def __str__(self):
        return self.username