from django.contrib import admin
from .models import Book, BookLibrary
# Register your models here.
admin.site.register(Book)
admin.site.register(BookLibrary)