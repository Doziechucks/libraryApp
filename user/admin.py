from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User






@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "first_name", "last_name", "email", "phone"),
            },
        ),
    )
    list_display = ["first_name", "last_name", "email", "phone"]
    list_display_links = ["email"]
    list_per_page = 10

# admin.site.register(Author)

# Register your models here.
