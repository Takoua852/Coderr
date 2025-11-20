from django.db import models
from django.conf import settings

class Profile(models.Model):
    """
    Model representing a user profile, linked one-to-one with a CustomUser.

    Attributes:
        user: One-to-one link to the associated user.
        first_name: User's first name (optional).
        last_name: User's last name (optional).
        file: Profile image uploaded to 'profiles/' directory.
        location: User's location (optional).
        tel: Contact phone number (optional).
        description: Short bio or description (optional).
        working_hours: Working hours for business users (optional).
        created_at: Timestamp when the profile was created (auto-set).
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, default='')
    last_name = models.CharField(max_length=50, blank=True, default='')
    file = models.ImageField(upload_to='profiles/', blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    tel = models.CharField(max_length=20, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=50, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the profile.
        """
        return f'{self.user.username} Profile'
    
  
    
