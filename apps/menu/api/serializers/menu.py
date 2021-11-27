from rest_framework import serializers

from apps.menu.models import Menu, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ("id", "menu", "dishes", "created_by", "created_at")


class MenuDishItemSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )


class MenuItemWithOutMenuSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(required=False)
    dishes = MenuDishItemSerializer(many=True, required=True, allow_empty=False)
    action = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = MenuItem
        fields = ("id", "dishes", "created_by", "created_at", "action")


class MenuSerializer(serializers.ModelSerializer):

    items = MenuItemWithOutMenuSerializer(
        write_only=True, required=True, many=True, allow_empty=False
    )

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

    def validate(self, data):
        """
        Validate the data and check the item information so, the user cannot add or edit items for other menus
        Args:
            data: dictionary of data to be validated

        Returns:
            dict with validated data
        """
        super().validate(data)
        if self.instance and self.instance.pk:
            items = data.get("items")
            err = {"items": []}
            for index, item in enumerate(items):
                err["items"].append(None)
                if "id" not in item:
                    continue
                if not MenuItem.objects.filter(
                    id=item["id"], menu=self.instance
                ).exists():
                    err["items"][index] = ["Menu item dont exists"]
            if any(err["items"]):
                raise serializers.ValidationError(err)
        return data

    def create(self, validated_data):
        """
        Create the menu and add the items to it
        Args:
            validated_data: dictionary of data to create menu and items
        Returns:
            Menu object
        """
        items = validated_data.pop("items")
        menu = super().create(validated_data)
        for item in items:
            MenuItem.objects.create(menu=menu, **item)
        return menu

    def update(self, instance, validated_data):
        """
        Update the menu and using action include in the item will add or remove the items from the menu send in the instance
        Args:
            instance: menu object
            validated_data: dictionary of data to be updated from the menu and the items
        Returns:
            Menu object
        """
        items = validated_data.pop("items")
        menu = super().update(instance, validated_data)
        for item in items:
            action = item.pop("action", "")
            if "id" in item:
                if action == "delete":
                    MenuItem.objects.get(id=item["id"]).delete()
                else:
                    MenuItem.objects.filter(id=item["id"]).update(**item)
            else:
                MenuItem.objects.create(menu=menu, **item)
        return menu
