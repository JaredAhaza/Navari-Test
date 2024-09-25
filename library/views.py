from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import *
from .models import *

# Create your views here.
def home(request):
    books = Book.objects.all()
    return render(request, 'library/index.html', {'object_list': books})

def books(request):
    books = Book.objects.all()
    return render(request, 'library/books.html', {'object_list': books})

@login_required
def usernav(request):
    print("User is logged in:", request.user.username)  # Check logged-in user
    try:
        # Attempt to retrieve the Customer associated with the logged-in user
        customer = Customer.objects.get(user=request.user)
        print("Customer found:", customer)  # Debug output
    except Customer.DoesNotExist:
        print("Customer does not exist for user:", request.user.username)  # Debug output
        return redirect('customersignup')  # Redirect to signup if no customer found
    
    context = {'customers': [customer]}  # Wrap in a list for iteration
    return render(request, 'includes/usernav.html', context)

# views.py
def search_books(request):
    books = Book.objects.all()  # Get all books initially

    # Retrieve search parameters from the GET request
    title = request.GET.get('title')
    author = request.GET.get('author')
    category = request.GET.get('category')

    # Apply filters if the search parameters are provided and are not default values
    if title and title != "Search Title":  # Ignore default value
        books = books.filter(title__icontains=title)
    if author and author != "Search Author":  # Ignore default value
        books = books.filter(author__icontains=author)
    if category and category != "All Categories":  # Ignore default value
        books = books.filter(category__icontains=category)

    return render(request, 'library/search_result.html', {'object_list': books})
