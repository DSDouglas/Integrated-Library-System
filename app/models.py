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
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    isbn = models.IntegerField()
    userid = models.CharField(max_length=255)
    onhold = models.BooleanField()
    checkout = models.BooleanField()
    def _str__(self):
        return [self.title, self.author, self.genre, self.isbn, self.userid, self.onhold, self.checkout]