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
            group = Group.objects.get(name='CUSTOMER')
            user.groups.add(group)
            
            return redirect('customerlogin')
        else:
            pass
            # If forms are not valid, pass the forms with errors back to the template
            
    else:
        user_form = CustomerUserForm()
        customer_form = CustomerForm()
        
    return render(request, 'accounts/register.html', {'user_form': user_form, 'customer_form': customer_form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/customerlogin')