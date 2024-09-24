from django.db.models.signals import post_save
from django.dispatch import receiver
from.models import *

@receiver(post_save, sender=Invoice)
def clear_debt_on_invoice_payment(sender, instance, **kwargs):
    if instance.is_paid:
        instance.clear_customer_debt()

@receiver(post_save, sender=Borrowing)
@receiver(post_save, sender=Returning)
def update_customer_debt(sender, instance, **kwargs):
    # Get the related customer
    customer = instance.customer if isinstance(instance, Borrowing) else instance.borrowing.customer

    # Update or create the Debt record for the customer
    debt, created = Debt.objects.get_or_create(customer=customer)
    debt.update_debt()