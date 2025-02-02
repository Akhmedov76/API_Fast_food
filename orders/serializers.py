import math

from menu.serializers import MenuItemSerializer
from rest_framework import serializers
from .models import Order, OrderItem, MenuItem


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_details = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'menu_item', 'menu_item_details', 'quantity', 'price')


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

    def validate_items(self, value):
        for item in value:
            menu_item_id = item.get('menu_item_id')
            quantity = item.get('quantity')
            if not menu_item_id or not quantity:
                raise serializers.ValidationError("Missing menu item ID or quantity.")
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)
                item['menu_item'] = menu_item
            except MenuItem.DoesNotExist:
                raise serializers.ValidationError(f"Menu item with ID {menu_item_id} does not exist.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total_amount = 0

        for item_data in items_data:
            menu_item = item_data.pop('menu_item')
            quantity = item_data.pop('quantity')
            price = menu_item.price * quantity
            total_amount += price
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price=price
            )

        order.total_amount = total_amount
        order.save()
        return order

    class Meta:
        model = Order
        fields = '__all__'
