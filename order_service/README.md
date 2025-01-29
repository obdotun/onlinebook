## Order Service
# Responsibility: Handle order creation and payment.

# Endpoints:

POST /orders - Create a new order.

GET /orders/:userId - Retrieve orders for a user.

Database: PostgreSQL (store order details like userId, bookId, quantity, status).

Steps:

Create a Django project:

bash
Copy
django-admin startproject order_service
cd order_service
Install required packages:

bash
Copy
pip install djangorestframework
Create an orders app:

bash
Copy
python manage.py startapp orders
Define the Order model in orders/models.py:

python
Copy
from django.db import models

class Order(models.Model):
    userId = models.CharField(max_length=100)
    bookId = models.CharField(max_length=100)
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, default='Pending')
Create views and serializers for CRUD operations in orders/views.py:

python
Copy
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
Add URLs in orders/urls.py:

python
Copy
from django.urls import path
from .views import OrderListCreateView, OrderRetrieveView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderRetrieveView.as_view(), name='order-detail'),
]
Run migrations and start the server:

bash
Copy
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 3003