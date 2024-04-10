import requests
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
from django.utils import timezone

from .models import Book, Fee


def get_book_description(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            for item in data["items"]:
                volume_info = item.get("volumeInfo")
                if volume_info:
                    title = volume_info.get("title", "No title available")
                    description = volume_info.get(
                        "description", "No description available"
                    )
                    if description:
                        return f"{title}: {description}"
            # If no description is found, return the first title
            first_item = data["items"][0]["volumeInfo"]
            title = first_item.get("title", "No title available")
            return title
    return "No description available"


def get_book_of_the_day():
    book = cache.get("book_of_the_day")
    if not book:
        total_books = Book.objects.count()
        random_book_index = randint(0, total_books - 1)
        book = Book.objects.all()[random_book_index]
        book.description = get_book_description(book.title)
        cache.set("book_of_the_day", book, timeout=86400)
    return book


def calculate_fee(due_date):
    # Calculate the fee amount based on the number of days overdue
    days_overdue = (timezone.now().date() - due_date).days
    fee_amount = max(
        0, days_overdue * 0.5
    )  # Charge 50 cents per day, capped at 0 if not overdue
    return fee_amount


@login_required
def place_hold_view(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.user_id == request.user.id:
        messages.error(
            request, "You cannot place a hold on a book you already have checked out."
        )
    elif book.on_hold:
        messages.error(request, "This book is already on hold.")
    else:
        book.on_hold = True
        book.hold_end = datetime.now() + timedelta(weeks=2)
        book.user_id = request.user.id  # Set user_id
        book.save()
        messages.success(request, "Book placed on hold successfully.")
        return HttpResponseRedirect(reverse("catalog"))  # Redirect back to catalog page


def index(request):
    book = get_book_of_the_day()
    return render(request, "index.html", {"book": book})


def catalog(request):
    books = Book.objects.all()
    return render(request, "catalog.html", {"books": books})


@login_required
def checked_out_books_view(request):
    if request.method == "POST":
        book_ids = request.POST.getlist("books")
        for book_id in book_ids:
            try:
                book = Book.objects.get(pk=book_id)
            except ObjectDoesNotExist:
                messages.error(request, "Book not found.")
                continue

            if book.checkout_date and book.user_id == request.user.id:
                messages.error(request, f"You already have '{book.title}' checked out.")
            elif book.checkout_date and book.user_id is not None:
                messages.error(
                    request, f"'{book.title}' is already checked out by another user."
                )
            else:
                # Remove the hold if it was placed by the current user
                if book.on_hold and book.user_id == request.user.id:
                    book.on_hold = False
                    book.hold_end = None
                    book.save()

                # Check out the book
                book.user_id = request.user.id
                book.checkout_date = timezone.now()
                book.due_date = datetime.now() + timedelta(weeks=2)
                book.save()
                messages.success(
                    request, f"Book '{book.title}' checked out successfully."
                )

        return HttpResponseRedirect(reverse("checked_out_books"))

    checked_out_books = Book.objects.filter(
        user_id=request.user.id, checkout_date__isnull=False
    )

    for book in checked_out_books:
        if book.due_date < timezone.now().date():
            # Book is overdue, calculate the fee
            fee_amount = calculate_fee(book.due_date)
            # Update or create a Fee object for the user and book
            fee, created = Fee.objects.update_or_create(
                book=book, user_id=request.user.id, defaults={"fee_amount": fee_amount}
            )
            if not created:
                fee.fee_amount = fee_amount
                fee.save()
    checked_out_books = Book.objects.filter(
        user_id=request.user.id, checkout_date__isnull=False
    ).prefetch_related("fee_set")

    return render(
        request, "checked_out_books.html", {"checked_out_books": checked_out_books}
    )


def checkin_view(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        book = Book.objects.get(pk=book_id)
        book.user_id = None
        book.on_hold = False
        book.hold_end = None
        book.save()

        # Delete the corresponding fee item
        Fee.objects.filter(book=book).delete()

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
