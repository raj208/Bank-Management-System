from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Account

class CustomUserAdmin(BaseUserAdmin):
    model = User

    def balance(self, obj):
        try:
            return obj.account.balance
        except Account.DoesNotExist:
            return "No Account"
    balance.short_description = 'Balance'

    list_display = ['username', 'email', 'is_admin', 'is_staff', 'balance'] 
    list_filter = ['is_admin', 'is_staff', 'is_superuser']
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_admin', 'is_customer')}),
    )

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'is_frozen']
    list_editable = ['is_frozen']  # allows inline freezing/unfreezing



admin.site.register(User, CustomUserAdmin)
admin.site.register(Account)
