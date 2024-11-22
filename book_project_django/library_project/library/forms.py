# library/forms.py
from django import forms
from .models import Book
from django.forms import DateInput

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date']
        widgets = {
            'published_date': DateInput(attrs={'type': 'date'}),  # Виджет с календарем
        }
