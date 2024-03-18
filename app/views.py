from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group



def index(request):
    return render(request, "index.html")

def catalog(request):
    books = Book.objects.all()
    return render(request, "catalog.html", {'books': books})

# def checkout_view(request):
#     if request.method == 'POST':
#         book_ids = request.POST.getlist('books')
#         for book_id in book_ids:
#             book = Book.objects.get(pk=book_id)
#             book.user_id = request.user.id  # Assuming user is authenticated
#             book.save()
#         # return HttpResponseRedirect('/success/')  # Redirect to success page
#     return render(request, 'checked_out_books.html')

def checked_out_books_view(request):
    if request.method == 'POST':
        book_ids = request.POST.getlist('books')
        for book_id in book_ids:
            book = Book.objects.get(pk=book_id)
            book.user_id = request.user.id  # Assuming user is authenticated
            book.save()
    checked_out_books = Book.objects.filter(user_id=request.user.id)
    return render(request, 'checked_out_books.html', {'checked_out_books': checked_out_books})

def checkin_view(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = Book.objects.get(pk=book_id)
        book.user_id = None
        book.save()
        return HttpResponseRedirect('/checked-out-books/')  # Redirect to checked out books page
    return HttpResponseRedirect('/')  # Redirect to home page if not a POST request
 
def create_account(request):
 
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
     
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
 
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            my_group = Group.objects.get(name='Patrons') 
            my_group.user_set.add(user)

            login(request, user)
            return HttpResponseRedirect('/')
         
        else:
            return render(request,'create_account.html',{'form':form})
     
    else:
        form = UserCreationForm()
        return render(request,'create_account.html',{'form':form})