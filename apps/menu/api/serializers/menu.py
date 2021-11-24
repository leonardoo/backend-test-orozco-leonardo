from abc import ABC

from rest_framework import serializers

from apps.menu.models import Menu, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ("id", "menu", "dishes", "created_by", "created_at")


class MenuDishItemSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class MenuItemWithOutMenuSerializer(serializers.ModelSerializer):

    dishes = MenuDishItemSerializer(many=True, required=True, allow_empty=False)

    class Meta:
        model = MenuItem
        fields = ("id", "dishes", "created_by", "created_at")


class MenuSerializer(serializers.ModelSerializer):

    items = MenuItemWithOutMenuSerializer(write_only=True, required=True, many=True, allow_empty=False)

    class Meta:
        model = Menu
        fields = (
            "id",
            "day",
            "status",
            "location",
            "created_by",
            "created_at",
            "updated_at",
            "items",
        )

    def create(self, validated_data):
        items = validated_data.pop("items")
        menu = super().create(validated_data)
        for item in items:
            MenuItem.objects.create(menu=menu, **item)
        return menu
