"""
URL configuration for the core API.

This module defines the URL routes for the core app endpoints.
Currently, it includes the endpoint to fetch general/base information.
"""

from django.urls import path
from .views import BaseInfoView

urlpatterns = [
    path('base-info/', BaseInfoView.as_view(), name="base-info")
]
