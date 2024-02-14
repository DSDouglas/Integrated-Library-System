from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "app/index.html")

def books(request):
    return render(request, "app/books.html")

def login(request):
    return render(request, "app/login.html")