##Book Service
#Responsibility: Manage book inventory.

#Endpoints:

GET /books - Retrieve all books.

POST /books - Add a new book.

PUT /books/:id - Update a book.

DELETE /books/:id - Delete a book.

Database: PostgreSQL (store book details like title, author, price).



Database: PostgreSQL (store book details like title, author, price).

Steps:

Create a Django project:

bash
Copy
django-admin startproject book_service
cd book_service
Install required packages:

bash
Copy
pip install djangorestframework
Create a books app:

bash
Copy
python manage.py startapp books
Define the Book model in books/models.py:

python
Copy
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
Create views and serializers for CRUD operations in books/views.py:

python
Copy
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
Add URLs in books/urls.py:

python
Copy
from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
Run migrations and start the server:

bash
Copy
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 3002