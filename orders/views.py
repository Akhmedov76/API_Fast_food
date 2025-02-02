import math
from datetime import timedelta
import geopy.distance

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from .models import Order, MenuItem
from .serializers import OrderSerializer, CreateOrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def calculate_delivery_time(self, distance, total_items):
        cooking_time = math.ceil(total_items / 4) * 5
        delivery_time = distance * 3
        return cooking_time + delivery_time

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rest_location = (
            settings.RESTAURANT_LOCATION['latitude'],
            settings.RESTAURANT_LOCATION['longitude']
        )

        delivery_lat = serializer.validated_data['latitude']
        delivery_lon = serializer.validated_data['longitude']
        client_location = (delivery_lat, delivery_lon)

        distance = geopy.distance.geodesic(rest_location, client_location).km
        print(f"Masofa: {distance} km")

        items_data = serializer.validated_data['items']
        total_items = sum(item['quantity'] for item in items_data)

        delivery_minutes = self.calculate_delivery_time(distance, total_items)
        estimated_delivery_time = timezone.now() + timedelta(minutes=delivery_minutes)

        order = serializer.save(
            user=request.user,
            distance=distance,
            estimated_delivery_time=estimated_delivery_time
        )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
