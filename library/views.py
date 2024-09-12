from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import *

# Create your views here.
def home(request):
    return render(request, 'library/index.html')

def books(request):
    return render(request, 'library/books.html')

@login_required
def usernav(request):
    try:
        customer = Customer.objects.get(user=request.user)
        print(customer)  # Add this line to check if the customer object is properly retrieved
        print(customer.user)  # Add this line to check if the customer.user property is accessible
        print(customer.customer_id)  # Add this line to check if the customer.customer_id property is accessible
    except Customer.DoesNotExist:
        return redirect('customersignup')
    context = {'customer': customer}
    return render(request, 'includes/usernav.html', context)