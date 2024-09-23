from django import forms
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'price', 'is_available', 'borrowed_by',  'book_picture')

        def __init__(self, *args, **kwargs):
            super(BookForm, self).__init__(*args, **kwargs)
            self.fields['borrowed_by'].queryset = Customer.objects.all()


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ('book', 'customer') 



class ReturningForm(forms.ModelForm):
    class Meta:
        model = Returning
        fields = ('borrowing', 'is_returned', 'is_late', 'is_damaged')

        def __init__(self, *args, **kwargs):
            super(ReturningForm, self).__init__(*args, **kwargs)