from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import Group
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

def CustomerSignup(request):
    if request.method == 'POST':
        user_form = CustomerUserForm(request.POST)
        customer_form = CustomerForm(request.POST) 
        if user_form.is_valid() and customer_form.is_valid():
            print("Forms are valid!")
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            print(f"Customer created: {customer.customer_id}")  # Log customer creation
            
            group = Group.objects.get(name='CUSTOMER')
            user.groups.add(group)
            
            return redirect('customerlogin')  # Redirect to login or another view
        else:
            print("Forms are invalid:", user_form.errors, customer_form.errors)  # Log form errors
            
    else:
        user_form = CustomerUserForm()
        customer_form = CustomerForm()
        
    return render(request, 'accounts/register.html', {'user_form': user_form, 'customer_form': customer_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/customerlogin')