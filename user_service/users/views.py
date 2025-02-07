from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
import jwt

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=request.data['email'])
        refresh = RefreshToken.for_user(user)
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)
        return response

class LoginView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response({'error': 'Invalid credentials'}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token
            return Response({'message': 'Successfully logged out'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ValidateTokenView(APIView):
    authentication_classes = [JWTAuthentication]  # Ensure JWT authentication is used
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        try:
            # Extract token from Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith("Bearer "):
                return Response({'error': 'Missing or invalid Authorization header'}, status=401)

            token = auth_header.split(" ")[1]  # Extract the actual token
            access_token = AccessToken(token)  # Validate the token

            return Response({'valid': True, 'user_id': access_token['user_id']}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=401)  # Return 401 for invalid token