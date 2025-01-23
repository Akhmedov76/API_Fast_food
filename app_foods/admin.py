from django.contrib import admin
from .models import User, MenuItemModel, OrderModel, OrderItemModel

admin.site.register(User)
admin.site.register(MenuItemModel)
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)
