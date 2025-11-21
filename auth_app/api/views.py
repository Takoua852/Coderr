from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from profile_app.models import Profile

class RegistrationView(APIView):

    """
    API view for user registration.

    Allows any user (even unauthenticated) to register by providing
    username, email, password, and type. Returns an authentication
    token upon successful registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):

        """
        Handle POST request for user registration.

        Steps:
        1. Validate incoming data with RegistrationSerializer.
        2. If valid, create the user and generate an authentication token.
        3. Return the token and user info in the response.
        4. If invalid, return serializer errors.
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            Profile.objects.get_or_create(user=saved_account)
            token, _ = Token.objects.get_or_create(user=saved_account)
            data = {
                "token": token.key,
                "username": saved_account.username,
                "email": saved_account.email,
                "user_id": saved_account.id
            }

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):

    """
    API view for user login.

    Allows any user (even unauthenticated) to log in by providing
    a valid username and password. Returns an authentication token
    upon successful login.
    """
    permission_classes = [AllowAny]

    def post(self, request):

        """
        Handle POST request for user login.

        Steps:
        1. Validate incoming data with LoginSerializer.
        2. If valid, retrieve the user and generate an authentication token.
        3. Return the token and user info in the response.
        4. If invalid, return serializer errors.
        """
        
        serializer  = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            data ={
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
