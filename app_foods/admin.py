from django.contrib import admin
from .models import UserModel, MenuItemModel, OrderModel, OrderItemModel

admin.site.register(UserModel)
admin.site.register(MenuItemModel)
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)
