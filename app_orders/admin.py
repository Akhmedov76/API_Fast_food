from django.contrib import admin

from app_orders.models import OrderModel, OrderItemModel

# Register your models here.
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)
