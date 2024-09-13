from django.db import models
from accounts.models import *

# Create your models here.
class Book(models.Model):
    CATEGORY = (
        ('Kids & Teens', 'Kids'),
        ('Science Fiction', 'Sci-Fi'),
        ('History', 'HS'),
        ('Religion', 'RG'),
        ('Health & Fitness', 'HF'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=30)
    publisher = models.CharField(max_length=50)

    price = models.CharField(max_length=50)
    category = models.CharField(blank=True, choices=CATEGORY, max_length=20)
    is_available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    borrow_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    book_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.title