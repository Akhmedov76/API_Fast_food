from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class UserRoleChoice(models.TextChoices):
    """
    UserRoleChoice is a class that contains choices for the user role.
    """
    ADMIN = "admin", "Admin"
    USER = "user", "User"
    COURIER = "courier", "Courier"


class UserStatusChoice(models.TextChoices):
    """
    UserStatusChoice is a class that contains choices for the user status.
    """
    ACTIVE = "active", "Active"
    DELETE = "delete", "Delete"
    INACTIVE = "inactive", "Inactive"


class OrderStatusChoice(models.TextChoices):
    """
    OrderStatusChoice is a class that contains choices for the order status.
    """
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class UserModel(AbstractUser):
    """
    UserModel is a custom user model that extends the AbstractUser model provided by Django.
    It has additional fields such as role, status.
    The role field is a CharField with choices to specify the user's role in the system.
    The status field is a CharField to specify the user's status in the system.
    """

    role = models.CharField(
        default=UserRoleChoice.USER,
        max_length=15,
        choices=UserRoleChoice.choices)
    status = models.CharField(
        default=UserStatusChoice.ACTIVE,
        max_length=15,
        choices=UserStatusChoice.choices)


class MenuItemModel(models.Model):
    """
    MenuItemModel is a model to represent the menu items available in the restaurant.
    It has fields such as name, price, description, is_available, created_at, and updated_at.
    The name field is a CharField with a maximum length of 255 characters.
    The price field is a DecimalField with a maximum of 6 digits and 2 decimal places.
    """

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
