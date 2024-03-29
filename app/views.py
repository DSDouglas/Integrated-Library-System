import wikipediaapi
from datetime import datetime, timedelta
from random import randint

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Book


def get_book_description(title):
    wiki_wiki = wikipediaapi.Wikipedia("Library-System (conman0503@gmail.com)", "en")
    page = wiki_wiki.page(title)
    if page.exists():
        return page.summary
    return "No description available"


def get_book_of_the_day():
    # Check if the book of the day is cached
    book = cache.get("book_of_the_day")
    if not book:
        # If not cached, select a random book from the database
        total_books = Book.objects.count()
        random_book_index = randint(0, total_books - 1)
        book = Book.objects.all()[random_book_index]
        book.description = get_book_description(book.title)
        # Cache the book with an expiration time of one day
        cache.set("book_of_the_day", book, timeout=86400)
    return book


@login_required
def place_hold_view(request, book_id):
    user_id = request.user.id
    if Book.objects.filter(user_id=user_id, on_hold=True).count() >= 4:
        messages.error(request, "You can only hold up to 4 books at a time.")
        return HttpResponseRedirect(reverse("catalog"))

    try:
        book = Book.objects.get(pk=book_id)
    except ObjectDoesNotExist:
        messages.error(request, "Book not found.")
        return HttpResponseRedirect(reverse("catalog"))

    if book.user_id == user_id:
        messages.error(
            request, "You cannot place a hold on a book you already have checked out."
        )
    elif book.on_hold:
        messages.error(request, "This book is already on hold.")
    else:
        book.on_hold = True
        book.hold_end = datetime.now() + timedelta(weeks=2)
        book.user_id = user_id
        book.save()
        messages.success(request, "Book placed on hold successfully.")
    return HttpResponseRedirect(reverse("catalog"))


def index(request):
    book = get_book_of_the_day()
    return render(request, "index.html", {"book": book})


def catalog(request):
    books = Book.objects.all()
    return render(request, "catalog.html", {"books": books})


def checked_out_books_view(request):
    if request.method == "POST":
        book_ids = request.POST.getlist("books")
        for book_id in book_ids:
            try:
                book = Book.objects.get(pk=book_id)
            except ObjectDoesNotExist:
                messages.error(request, "Book not found.")
                continue

            if book.user_id == request.user.id:
                messages.error(request, f"You already have '{book.title}' checked out.")
            elif book.on_hold and book.user_id != request.user.id:
                messages.error(request, f"'{book.title}' is on hold by another user.")
            else:
                book.user_id = request.user.id
                book.save()
                messages.success(
                    request, f"Book '{book.title}' checked out successfully."
                )

                # Remove the hold if it was placed by the current user
                if book.on_hold:
                    book.on_hold = False
                    book.hold_end = None
                    book.save()
        return HttpResponseRedirect(reverse("checked_out_books"))

    checked_out_books = Book.objects.filter(user_id=request.user.id)
    return render(
        request, "checked_out_books.html", {"checked_out_books": checked_out_books}
    )


def checkin_view(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        book = Book.objects.get(pk=book_id)
        book.user_id = None
        book.save()
        return HttpResponseRedirect(
            reverse("checked_out_books")
        )  # Redirect to checked out books page
    return HttpResponseRedirect(
        reverse("index")
    )  # Redirect to home page if not a POST request


def create_account(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            my_group = Group.objects.get(name="Patrons")
            my_group.user_set.add(user)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "create_account.html", {"form": form})

    else:
        form = UserCreationForm()
        return render(request, "create_account.html", {"form": form})
