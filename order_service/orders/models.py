from django.db import models

class Order(models.Model):
    userId = models.CharField(max_length=100)
    bookId = models.CharField(max_length=100)
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, default='Pending')