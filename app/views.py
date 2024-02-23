from django.shortcuts import render
from django.http import HttpResponse
from .models import Book


def index(request):
    return render(request, "app/index.html")

def catalog(request):
    books = Book.objects.all()
    return render(request, "app/catalog.html", {'books': books})

def login(request):
    return render(request, "app/login.html")