from django.urls import path
from .views import ProfileDetailAPIView, ProfilesListAPIView

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profiles/business/', ProfilesListAPIView.as_view(),
         {'type': 'business'}, name='profile-business'),
    path('profiles/customer/', ProfilesListAPIView.as_view(),
         {'type': 'customer'}, name='profile-customer'),
]
