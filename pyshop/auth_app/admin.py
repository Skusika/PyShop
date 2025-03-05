from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)

# Register your models here.

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     """
#     Класс для настройки отображения пользователя в админке.
#     """
#
#     list_display = ("last_name", "first_name", "email")
#     list_display_links = ("last_name", "first_name", "email")
#     ordering = ["last_name"]
