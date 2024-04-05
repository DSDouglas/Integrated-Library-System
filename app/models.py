from django.db import models


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Admin"


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    pub_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    publisher = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey("Patron", models.DO_NOTHING, blank=True, null=True)
    on_hold = models.IntegerField(blank=True, null=True)
    hold_end = models.DateField(blank=True, null=True)
    checkout_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Book"


class Librarian(models.Model):
    librarian_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Librarian"


class Patron(models.Model):
    patron_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Patron"


class Fee(models.Model):
    fee_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    fee_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    user_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Fee"
