from decimal import Decimal
from django.db import models
from accounts.models import *
from django.core.exceptions import ValidationError

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
            if hasattr(borrowing, 'returning'):
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
        # Calculate fine based on lateness and damage
        self.fine = (100 if self.is_late else 0) + (100 if self.is_damaged else 0)

        # Call the parent save method to ensure object is saved
        super().save(*args, **kwargs)

        if self.is_returned:
            # Mark the book as available again
            self.borrowing.book.is_available = True
            self.borrowing.book.save()

            # Get or create the customer's debt object
            debt, created = Debt.objects.get_or_create(customer=self.borrowing.customer)

            # Update the customer's total debt after the return
            debt.update_debt()

    def calculate_total_fee(self):
        # Total fee includes the book price and the fine
        return self.borrowing.book_price + self.fine



class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_generated = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice for {self.customer.user} - {self.date_generated.strftime('%Y-%m-%d')}"

    def generate_invoice_for_customer(self):
        borrowings = Borrowing.objects.filter(customer=self.customer)
        total_amount = Decimal(0)
        invoice_details = []

        for borrowing in borrowings:
            total_fee = borrowing.returning.calculate_total_fee() if hasattr(borrowing, 'returning') else borrowing.book_price
            total_amount += total_fee
            invoice_details.append({
                'book': borrowing.book.title,
                'fine': borrowing.returning.fine if hasattr(borrowing, 'returning') else 0,
                'total_fee': total_fee
            })

        invoice = Invoice.objects.create(customer=self.customer, total_amount=total_amount)
        return {
            'invoice': invoice,
            'invoice_details': invoice_details,
            'total_amount': total_amount,
        }

    def clear_customer_debt(self):
        """Clears the debt for the customer associated with this invoice."""
        debt, created = Debt.objects.get_or_create(customer=self.customer)
        debt.total_debt = 0
        debt.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_paid:
            # Clear customer debt if the invoice is marked as paid
            self.clear_customer_debt()
