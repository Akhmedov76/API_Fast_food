from django.contrib import admin
from .models import Order, OrderItem
from django.utils.translation import gettext_lazy as _


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'total_amount', 'distance', 'estimated_delivery_time')

    list_filter = ('status', 'created_at', 'distance', 'estimated_delivery_time')

    ordering = ('-created_at', )


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
