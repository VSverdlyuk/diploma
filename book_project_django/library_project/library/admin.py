# library/admin.py
from django.contrib import admin
from .models import Book

# Регистрация модели Book
admin.site.register(Book)
    