from django.db import models

from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    ROLE_CHOICES = [(
        ('admin', 'Admin'),
        ('user', 'User'),
        ('courier', 'Courier'),
    )]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
    )

    @property
    def is_admin(self):
        return self.role == 'admin'


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
        ordering = ['-created_at']


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    distance_km = models.FloatField()
    is_accepted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
