from rest_framework import serializers

from app_menu.models import MenuItemModel


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemModel
        fields = '__all__'
