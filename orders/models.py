import asyncio
from datetime import timedelta
from django.db import models
from django.conf import settings
from geopy.distance import geodesic
from rest_framework import serializers

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
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    distance = models.FloatField(help_text='Distance in kilometers', null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_estimated_delivery_time(self):
        preparation_time = (self.menu_item.count() // 4) * 5

        delivery_time = self.distance * 3

        total_time_minutes = preparation_time + delivery_time

        estimated_delivery_time = self.created_at + timedelta(minutes=total_time_minutes)
        return estimated_delivery_time

    def save(self, *args, **kwargs):
        if (self.latitude is None or self.longitude is None) and self.delivery_address:
            coordinates = asyncio.run(get_coordinates_from_address(self.delivery_address))
            if coordinates and isinstance(coordinates, tuple):
                self.latitude, self.longitude = coordinates
        if self.latitude is not None and self.longitude is not None:
            rest_location = (
                settings.RESTAURANT_LOCATION['latitude'],
                settings.RESTAURANT_LOCATION['longitude']
            )
            client_location = (self.latitude, self.longitude)
            self.distance = geodesic(rest_location, client_location).km

        self.estimated_delivery_time = self.calculate_estimated_delivery_time()

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
        return f"{self.quantity}x {self.menu_item.name}"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
