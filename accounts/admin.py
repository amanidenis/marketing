from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Corrected import statement
from .models import Account

class AccountAdmin(UserAdmin):  # Ensure class name is correctly capitalized
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    urderiing = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)