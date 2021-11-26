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
        items = validated_data.pop("items")
        menu = super().create(validated_data)
        for item in items:
            MenuItem.objects.create(menu=menu, **item)
        return menu

    def update(self, instance, validated_data):
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
