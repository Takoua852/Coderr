from rest_framework import serializers
from profile_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.


    Allows reading and updating profile-specific fields:
        - first_name, last_name, file, location, tel, description, working_hours, email
        - created_at (read-only)
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', required=False)
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

    def update(self, instance, validated_data):
        """
        Update Profile instance with validated data.

        Handles nested user data for email updates.
        """
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')

        if email:
            instance.user.email = email
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
