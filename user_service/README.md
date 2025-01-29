## User Service
# Responsibility: Handle user registration, login, and profile management.

# Endpoints:

POST /register - Register a new user.

POST /login - Authenticate a user and return a JWT token.

GET /profile - Get user profile (protected route).

Database: PostgreSQL (store user details like name, email, password).

Steps:

Create a Django project:

bash
Copy
django-admin startproject user_service
cd user_service
Install required packages:

bash
Copy
pip install djangorestframework djangorestframework-simplejwt
Create a users app:

bash
Copy
python manage.py startapp users
Update settings.py:

python
Copy
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'users',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
Define the User model in users/models.py:

python
Copy
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
Create serializers and views for registration, login, and profile in users/views.py:

python
Copy
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LoginView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=400)

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
Add URLs in users/urls.py:

python
Copy
from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
Run migrations and start the server:

bash
Copy
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 3001