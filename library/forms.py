from django import forms
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'price', 'is_available', 'borrowed_by', 'borrow_date',  'book_picture', 'return_date')

        def __init__(self, *args, **kwargs):
            super(BookForm, self).__init__(*args, **kwargs)
            self.fields['borrowed_by'].queryset = Customer.objects.all()


class BorrowBookForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())