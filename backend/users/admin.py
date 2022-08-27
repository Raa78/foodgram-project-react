from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from foodgram.config import EMPTY_VALUE_DISPLAY

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = (
        'username',
        'email',
    )
    search_fields = (
        'username',
        'last_name',
        'email',
    )
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'user',
    )
    search_fields = (
        'user',
        'author',
    )
    list_filter = (
        'user',
        'author',
    )
    empty_value_display = EMPTY_VALUE_DISPLAY
