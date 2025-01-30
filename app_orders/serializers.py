from rest_framework import serializers
from app_orders.models import OrderModel, OrderItemModel


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(required=True)
    lon = serializers.FloatField(required=True)

    class Meta:
        model = OrderItemModel
        fields = "__all__"
