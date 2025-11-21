from .serializers import ProfileSerializer, ProfileBusinessSerializer, ProfileCustomerSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from profile_app.models import Profile
from django.shortcuts import get_object_or_404
from auth_app.models import CustomUser
from .permissions import IsOwner


class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving or updating a user's profile.

    Features:
    - GET: Retrieve a profile (any authenticated user can view)
    - PUT/PATCH: Update a profile (only the owner can update)
    - Automatically creates a Profile if it does not exist
    """
    serializer_class = ProfileSerializer

    def get_object(self):
        """
        Retrieve the Profile object for the given user ID.
        If the Profile does not exist, create it automatically.

        Returns:
            Profile instance
        """
        user_id = self.kwargs['pk']
        user = get_object_or_404(CustomUser, pk=user_id)
        profile, created = Profile.objects.get_or_create(user=user)
        self.check_object_permissions(self.request, profile)
        return profile
    
    def get_permissions(self):
        """
        Return different permissions depending on HTTP method:
        - PUT/PATCH: Only the owner can update
        - GET: Any authenticated user can view
        """
        if self.request.method in ['PUT', 'PATCH']:
            return [IsOwner()]
        return [IsAuthenticated()]

class ProfilesListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.select_related('user')
        user_type = self.kwargs.get('type')
        if user_type in ['business', 'customer']:
            queryset = queryset.filter(user__type=user_type)
        return queryset

    def get_serializer_class(self):
        user_type = self.kwargs.get('type')
        if user_type == 'business':
            return ProfileBusinessSerializer
        elif user_type == 'customer':
            return ProfileCustomerSerializer
        return ProfileSerializer
    