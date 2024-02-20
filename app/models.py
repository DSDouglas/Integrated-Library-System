from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.user_id 

class Admin(models.Model):
    user_id = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    checkout_limit = models.IntegerField()
    def __str__(self):
        return self.user_id

class Librarian(models.Model):
    user_id = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.user_id

class Patron(models.Model):
    user_id = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.user_id

class Book(models.Model):
    isbn = models.IntegerField()
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_year = models.IntegerField()
    publisher = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    userid = models.CharField(max_length=255)
    onhold = models.BooleanField()
    hold_end = models.DateField()
    checkout_date = models.IntegerField()
    due_date = models.DateField()
    
    def _str__(self):
        return [self.title, self.author, self.genre, self.isbn, self.userid, self.onhold, self.checkout]

class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
