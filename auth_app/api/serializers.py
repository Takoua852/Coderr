from rest_framework import serializers
from auth_app.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration.

    Handles validation and creation of a new user, including:
    - Password confirmation
    - Unique email check
    - Setting the hashed password
    """

    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email',
                  'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):

        """
        Custom validation logic.

        Ensures that:
        - Password and repeated_password match
        - Email is unique in the database
        """

        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email is already in use.")

        return data

    def create(self, validated_data):

        """
        Create a new CustomUser instance after validation.

        - Removes repeated_password from the validated data
        - Hashes the password before saving
        """

        validated_data.pop('repeated_password')
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):

    """
    Serializer for user login.

    Handles validation of username and password and ensures
    that the user exists and the password is correct.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        """
        Custom validation for login.

        Steps:
        1. Check if the user with the given username exists.
        2. Verify that the password matches.
        3. Attach the user instance to the validated data for later use.
        """
        
        username = data.get('username')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password.")

        data['user'] = user
        return data
