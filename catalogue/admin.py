from django.contrib import admin
from . import models


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "genre", "language", "isbn"]
    # list_filter = ["isbn"]
    search_fields = ["title", "isbn"]
    list_per_page = 10


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "dob", "dod"]
    search_fields = ["first_name", "last_name"]

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(models.BookImage)
class BookImageAdmin(admin.ModelAdmin):
    list_display = ["image", "book"]
    search_fields = ["image"]


# admin.site.register(models.Book)
# admin.site.register(models.Genre)
# admin.site.register(models.BookInstance)
# admin.site.register(models.Language)
# admin.site.register(models.Author)

# Register your models here.
