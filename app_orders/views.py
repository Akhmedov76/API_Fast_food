from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from app_orders.models import OrderModel, OrderItemModel
from app_orders.serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItemModel.objects.all()
    serializer_class = OrderItemSerializer