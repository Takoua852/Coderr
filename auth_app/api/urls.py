"""
urls.py

This module defines the URL patterns for the authentication app,
including user registration and login functionality.

Each URL is connected to a class-based view.
"""

from django.urls import path
from .views import RegistrationView,LoginView

urlpatterns = [
   path('registration/', RegistrationView.as_view(), name='registration'),
   path('login/', LoginView.as_view(), name='login')
]