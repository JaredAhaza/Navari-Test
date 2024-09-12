from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from . import models
from django.core.exceptions import ValidationError

class CustomerUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        group = Group.objects.get(name='CUSTOMER')
        user.groups.add(group)
        return user

class SuperUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = True
        user.save()
        group = Group.objects.get(name='CUSTOMER')
        group.user_set.remove(user)
        return user

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('email', 'phone_number', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if models.Customer.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    