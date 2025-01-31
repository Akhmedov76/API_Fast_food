import asyncio

from django.db import models
from django.conf import settings
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

from menu.models import MenuItem
from utils.geolocations import get_coordinates_from_address


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('on_delivery', 'On Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    distance = models.FloatField(help_text='Distance in kilometers', null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def save(self, *args, **kwargs):
        if self.delivery_address and not (self.latitude and self.longitude):
            try:
                geolocator = Nominatim(user_agent="my_app")
                location = geolocator.geocode(self.delivery_address)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except GeocoderTimedOut:
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} in Order #{self.order.id}"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
