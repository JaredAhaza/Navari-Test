from decimal import Decimal
from django.db import models
from accounts.models import *
from django.core.exceptions import ValidationError

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

    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(blank=True, choices=CATEGORY, max_length=20)
    is_available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    borrow_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    book_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    fee = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=7)
    is_returned = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)
    is_damaged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.customer.user}"
    
    def save(self, *args, **kwargs):
        if self.book:
            self.fee = self.book.price
        customer_debt = Borrowing.objects.filter(customer=self.customer, is_returned=False).aggregate(fee_sum=models.Sum('fee')).get('fee_sum', 0) or 0
        if customer_debt + self.fee > 500:
            raise ValidationError("You have exceeded your borrowing limit of 500Ksh")
        super().save(*args, **kwargs)


    def calculate_total_debt(self):
        return Borrowing.objects.filter(customer=self.customer, is_returned=False).aggregate(fee_sum=models.Sum('fee'))('fee_sum', 0)
    
    def calculate_additional_fees(self):
        additional_fees = 0
        if self.is_late:
            additional_fees += 100
        if self.is_damaged:
            additional_fees += 100
        return additional_fees