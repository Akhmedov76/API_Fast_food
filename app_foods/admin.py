from django.contrib import admin
from django.contrib.auth.models import Group

from .models import UserModel, MenuItemModel, OrderModel, OrderItemModel

admin.site.register(UserModel)
admin.site.register(MenuItemModel)
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)
admin.site.unregister(Group)