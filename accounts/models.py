from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    customer_id = models.CharField(max_length=3, primary_key=True)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(User, related_name='customer_groups')
    user_permissions = models.ManyToManyField(User, related_name='customer_permissions')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            last_customer = Customer.objects.order_by('customer_id').last()
            if last_customer:
                next_id = int(last_customer.customer_id[2:]) + 1
            else:
                next_id = 1
            self.customer_id = f"ML{next_id:03d}"
        super().save(*args, **kwargs)