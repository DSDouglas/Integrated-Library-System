from django.contrib import admin

from .models import Admin, Book

admin.site.register([Book, Admin])
