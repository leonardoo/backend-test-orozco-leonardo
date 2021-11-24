from rest_framework import serializers

from apps.menu.business import can_user_select_lunch
from apps.menu.models import MenuSelectByUser


class MenuSelectByUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSelectByUser
        fields = (
            "id",
            "menu",
            "user",
            "created_at",
            "item",
            "comments",
        )

    def validate(self, data):
        data = super().validate(data)
        select = MenuSelectByUser.objects.filter(user=data["user"], menu=data["menu"])
        if select.exists():
            raise serializers.ValidationError("You have already selected this menu")
        if not can_user_select_lunch(
            timezone_data=self.timezone_data, menu=data["menu"]
        ):
            raise serializers.ValidationError("You can't select lunch")
        return data
