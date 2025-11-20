
"""
URLs for the Profiles app.

Includes routes for:
- Retrieving a single profile by ID
- Listing profiles filtered by user type ('customer' or 'business')
"""

from django.urls import path
from .views import ProfileDetailAPIView, ProfilesListAPIView

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profiles/<str:type>/', ProfilesListAPIView.as_view(), name='profile-list-by-type'),
]
