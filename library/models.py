from django.db import models
from accounts.models import *

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=30)
    publisher = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    borrow_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
