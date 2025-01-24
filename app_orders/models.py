from django.db import models

from app_menu.models import MenuItemModel
from app_user.models import UserModel, OrderStatusChoice


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    distance_km = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        default=OrderStatusChoice.PENDING,
        max_length=15,
        choices=OrderStatusChoice.choices
    )

    def calculate_delivery_time(self):
        preparation_time = 5 * (self.order_items.count() // 4 + 1)
        delivery_time = self.distance_km * 3
        return preparation_time + delivery_time

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItemModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
