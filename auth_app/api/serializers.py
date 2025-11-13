from rest_framework import serializers
from auth_app.models import CustomUser



class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email',
                  'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
                raise serializers.ValidationError("Passwords do not match.")

        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email is already in use.")

        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
     username = serializers.CharField()
     password = serializers.CharField(write_only=True)

     def validate(self, data):
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
