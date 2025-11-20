from rest_framework import serializers
from profile_app.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    Includes read-only fields from the related user:
        - username
        - email
        - id (user)
        - type (user type: customer or business)
    
    Allows reading and updating profile-specific fields:
        - first_name, last_name, file, location, tel, description, working_hours
        - created_at (read-only)
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at',
        ]

class ProfileBusinessSerializer(ProfileSerializer):
    """
    Serializer for business user profiles, extending ProfileSerializer.

    Includes fields relevant for business users:
        - user, username, first_name, last_name
        - file, location, tel, description, working_hours
        - type (user type: business)
    """
    class Meta(ProfileSerializer.Meta):
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type'
        ]

class ProfileCustomerSerializer(ProfileSerializer):
    """
    Serializer for customer user profiles, extending ProfileSerializer.

    Includes fields relevant for customer users:
        - user, username, first_name, last_name
        - file
        - type (user type: customer)
    """
    class Meta(ProfileSerializer.Meta):
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'type'
        ]

