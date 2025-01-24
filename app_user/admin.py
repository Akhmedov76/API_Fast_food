from django.contrib import admin
from django.contrib.auth.models import Group

from app_user.models import UserModel

# Register your models here.
admin.site.register(UserModel)
admin.site.unregister(Group)
