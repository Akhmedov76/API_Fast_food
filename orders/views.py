from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from menu.models import MenuItem


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.role == 'waiter':
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        return round(distance, 2)

    def calculate_delivery_time(self, distance, total_items):

        cooking_batches = (total_items + settings.COOKING_CAPACITY['dishes_per_batch'] - 1) // \
                          settings.COOKING_CAPACITY['dishes_per_batch']
        cooking_time = cooking_batches * settings.COOKING_CAPACITY['minutes_per_batch']


        delivery_time = distance * settings.DELIVERY_SPEED['minutes_per_km']

        return cooking_time + delivery_time

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Calculate distance
        rest_lat = settings.RESTAURANT_LOCATION['latitude']
        rest_lon = settings.RESTAURANT_LOCATION['longitude']
        delivery_lat = serializer.validated_data['latitude']
        delivery_lon = serializer.validated_data['longitude']

        distance = self.calculate_distance(rest_lat, rest_lon, delivery_lat, delivery_lon)

        items_data = serializer.validated_data['items']
        total_items = sum(item['quantity'] for item in items_data)
        total_amount = 0

        delivery_fee = distance * 2
        delivery_minutes = self.calculate_delivery_time(distance, total_items)
        estimated_delivery_time = datetime.now() + timedelta(minutes=delivery_minutes)

        order = Order.objects.create(
            user=request.user,
            delivery_address=serializer.validated_data['delivery_address'],
            delivery_latitude=delivery_lat,
            delivery_longitude=delivery_lon,
            distance=distance,
            delivery_fee=delivery_fee,
            estimated_delivery_time=estimated_delivery_time,
            total_amount=total_amount
        )

        for item_data in items_data:
            menu_item = MenuItem.objects.get(id=item_data['menu_item'])
            quantity = item_data['quantity']
            price = menu_item.price * quantity
            total_amount += price

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price=price
            )

        order.total_amount = total_amount + delivery_fee
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)