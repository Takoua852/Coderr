from django.db import models
from django.contrib.auth.models import AbstractUser

    
class CustomUser(AbstractUser):

    """
    Custom user model extending Django's AbstractUser.

    Adds a user type field to differentiate between customers and businesses,
    and enforces a unique email address for each user.
    """

    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    REQUIRED_FIELDS = ['email', 'type']

    def __str__(self):
        """
        String representation of the user.

        Returns the username.
        """
        return self.username