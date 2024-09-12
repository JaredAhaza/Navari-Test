from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('customersignup', views.CustomerSignup, name='customersignup'),
    path('customerlogin', LoginView.as_view(template_name='accounts/customerlogin.html'), name='customerlogin'),
]