from rest_framework import serializers
from profile_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
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
    class Meta(ProfileSerializer.Meta):
        fields = [
            'user', 'username', 'first_name', 'last_name', 
            'file', 'location', 'tel', 'description', 
            'working_hours', 'type'
        ]

class ProfileCustomerSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = [
            'user', 'username', 'first_name', 'last_name', 
            'file', 'type'
        ]