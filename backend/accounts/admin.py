from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'is_active')
    list_display_links = ('full_name', 'email')
    list_filter = ('email', 'is_staff', 'is_active')
    search_fields = ('email',)
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('username', 'first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_active',
                       'is_staff',
                       'is_superuser',
                       'groups',
                       'user_permissions')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'password1',
                       'password2',
                       'is_staff',
                       'is_active')
        }),
    )


admin.site.register(User, UserAdmin)
