from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
