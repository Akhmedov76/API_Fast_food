from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('courier', 'Courier'),
        ('user', 'User'),

    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class MenuItemModel(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    distance_km = models.FloatField()
    is_accepted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def delivery_time(self):
        preparation_time = 5 * (self.items.count() // 4 + 1)
        delivery_time = self.distance_km * 3
        return preparation_time + delivery_time

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItemModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
