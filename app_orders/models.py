import asyncio
from django.db import models
from app_menu.models import MenuItemModel
from app_user.models import UserModel


class OrderStatusChoice(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    lat = models.CharField(max_length=250, null=True, blank=True)
    lon = models.CharField(max_length=250, null=True, blank=True)
    distance_km = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        max_length=15,
        choices=OrderStatusChoice.choices,
        default=OrderStatusChoice.PENDING
    )

    def __str__(self):
        return f"Order by {self.user.username}"

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
