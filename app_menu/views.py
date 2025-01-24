from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app_menu.models import MenuItemModel
from app_menu.serializers import MenuItemSerializer
from app_orders.permissions import IsWaiter
from app_user.permissions import IsAdmin


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItemModel.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsWaiter]
