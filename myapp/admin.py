from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Account

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ['username', 'email', 'is_admin', 'is_staff', 'is_superuser']
    list_filter = ['is_admin', 'is_staff', 'is_superuser']
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_admin', 'is_customer')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Account)
