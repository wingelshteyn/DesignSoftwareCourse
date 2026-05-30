from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Zone


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created_at"]
    search_fields = ["name"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "role", "zone", "is_active"]
    list_filter = ["role", "zone", "is_active"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("MDT Role & Zone", {"fields": ("role", "zone")}),
    )
