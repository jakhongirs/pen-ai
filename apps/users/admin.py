from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "is_available")
    list_filter = ("is_available",)
    search_fields = ("email", "first_name", "last_name")
