from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Book, Fee
from .views import calculate_fee, get_book_description


class LibraryAppTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.book = Book.objects.create(title="Test Book", author="Test Author")

    def test_get_book_description(self):
        description = get_book_description("Python")
        self.assertTrue(len(description) > 0)

    def test_calculate_fee(self):
        due_date = datetime.now() - timedelta(days=5)
        fee_amount = calculate_fee(due_date)
        self.assertEqual(fee_amount, 2.5)  # Assuming 50 cents per day

        due_date = datetime.now() + timedelta(days=1)
        fee_amount = calculate_fee(due_date)
        self.assertEqual(fee_amount, 0)  # Book is not overdue

    def test_place_hold_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("place_hold", args=[self.book.book_id]))
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_checked_out_books_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("checked_out_books"))
        self.assertEqual(response.status_code, 200)  # Check if the page loads

    def test_checkin_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("checkin"), {"book_id": self.book.book_id})
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_create_account_view(self):
        url = reverse("create_account")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_account_post(self):
        url = reverse("create_account")
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, 302
        )  # Redirects after successful form submission

        # Check if the user was created and added to the correct group
        self.assertTrue(User.objects.filter(username="testuser").exists())
        user = User.objects.get(username="testuser")
        self.assertTrue(user.groups.filter(name="Patrons").exists())

    def test_create_account_invalid_form(self):
        url = reverse("create_account")
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "invalidpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, 200
        )  # Form should not redirect on invalid data
        self.assertContains(response, "password2")  # Check if form errors are displayed
