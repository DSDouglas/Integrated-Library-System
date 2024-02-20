from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "app/index.html")

def catalog(request):
    return render(request, "app/catalog.html")

def login(request):
    return render(request, "app/login.html")