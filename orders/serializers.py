import math
from rest_framework import serializers
from menu.serializers import MenuItemSerializer
from .models import Order, OrderItem, MenuItem


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_details = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'menu_item', 'menu_item_details', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'status', 'estimated_delivery_time', 'total_amount')


class CreateOrderSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    delivery_address = serializers.CharField(max_length=255)
    items = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'status': {'read_only': True},
            'estimated_delivery_time': {'read_only': True},
            'total_amount': {'read_only': True},
        }
