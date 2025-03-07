from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from users.models import User
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (_('User info'), {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    search_fields = (_('username'), _('email'), _('phone'))
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

admin.site.site_header = _("Restaurant")
admin.site.site_title = _("My Admin")
admin.site.index_title = _("Welcome to My Dashboard")
