import uuid
from django.utils import timezone

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User




# Create your models here.

class Genre(models.Model):
    GENRE_CHOICES = (
        ("R", "ROMANCE"),
        ("D", "COMEDY"),
        ("P", "POLITICS"),
        ("F", "FINANCE"),
    )
    name = models.CharField(max_length=1, choices=GENRE_CHOICES, default="F", unique=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    LANGUAGES = (
        ("Y", "YORUBA"),
        ("H", "HAUSA"),
        ("I", "IGBO"),
    )
    name = models.CharField(max_length=2, choices=LANGUAGES, default="Y")
    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    dob = models.DateField(blank=False, null=False, default=timezone.now)
    dod = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Book(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, default=1)
    author = models.ManyToManyField(Author, related_name="books")

    def __str__(self):
        return self.title



# class Category(models.Model):
#     title = models.CharField(max_length=100)
#     author = models.CharField(max_length=100)
#     summary = models.TextField()
#     isbn = models.CharField(max_length=11, unique=True)
#     genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.title




class BookInstance(models.Model):
    LOAN_STATUS = (
        ("A", "AVAILABLE"),
        ("B", "BORROWED"),
        ("M", "MAINTENANCE"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, default="A")
    return_date = models.DateTimeField(null=False, blank=True)
    comments = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class BookImage(models.Model):
    image = models.ImageField(upload_to="book/image", blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.image.url
