# Generated by Django 4.2.10 on 2024-02-23 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_book_date_published_remove_book_publisher'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterModelOptions(
            name='admin',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='librarian',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='patron',
            options={'managed': False},
        ),
    ]
