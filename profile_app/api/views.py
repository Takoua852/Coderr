from .serializers import ProfileSerializer, ProfileBusinessSerializer, ProfileCustomerSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from profile_app.models import Profile
from django.shortcuts import get_object_or_404
from auth_app.models import CustomUser
from .permissions import IsOwnerOrReadOnly


class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def get_object(self):
        user_id = self.kwargs['pk']
        user = get_object_or_404(CustomUser, pk=user_id)
        profile, created = Profile.objects.get_or_create(user=user)
        return profile


class ProfilesListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.select_related('user')
        user_type = self.kwargs.get('type') or self.request.query_params.get('type')
        if user_type in ['business', 'customer']:
            queryset = queryset.filter(user__type=user_type)
        return queryset

    def get_serializer_class(self):
        user_type = self.kwargs.get('type') or self.request.query_params.get('type')
        if user_type == 'business':
            return ProfileBusinessSerializer
        elif user_type == 'customer':
            return ProfileCustomerSerializer
        return ProfileSerializer