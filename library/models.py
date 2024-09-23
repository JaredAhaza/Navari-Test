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
    book_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.title


class Debt(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    total_debt = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return f"Debt for {self.customer.user}: {self.total_debt} shillings"
    
    def update_debt(self):
        borrowings = Borrowing.objects.filter(customer=self.customer)
        total_debt = Decimal(0)
        for borrowing in borrowings:
            if hasattr(borrowing, 'returning') and borrowing.returning.is_returned:
                total_debt += borrowing.returning.calculate_total_fee()
            else:
                total_debt += borrowing.book_price
        self.total_debt = total_debt
        self.save()
    
class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True, editable=False)
    book_price = models.DecimalField(max_digits=7, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.customer.user}"
    
    def save(self, *args, **kwargs):
        if self.book:
            self.book_price = self.book.price
        debt, created = Debt.objects.get_or_create(customer=self.customer)
        debt.update_debt()
        if debt.total_debt > 500:
            raise ValidationError("Customer has a debt exceeding 500 shillings, cannot borrow more books")
        if self.book:
            self.book_price = self.book.price
            self.book.is_available = False
            self.book.save()
        super().save(*args, **kwargs)
        debt.update_debt()

    
class Returning(models.Model):
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE)
    is_returned = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)
    is_damaged = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=7, decimal_places=2, default=0)


    def save(self, *args, **kwargs):
        self.fine = (100 if self.is_late else 0) + (100 if self.is_damaged else 0)
        super().save(*args, **kwargs)

        if self.is_returned:
            self.borrowing.book.is_available = True
            self.borrowing.book.save()
            debt, created = Debt.objects.get_or_create(customer=self.borrowing.customer)
            total_deduction = self.borrowing.book_price + self.fine
            debt.total_debt -= total_deduction
            debt.update_debt()
        super().save(*args, **kwargs)

    def calculate_total_fee(self):
        return self.borrowing.book_price + self.fine
    