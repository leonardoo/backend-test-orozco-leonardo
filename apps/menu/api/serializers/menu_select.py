from django.contrib.auth.models import User
from rest_framework import serializers

from apps.menu.business import can_user_select_lunch
from apps.menu.models import MenuSelectByUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


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
        """
        Check if the user can select a item for lunch, this will validate that first the user had not selected any element for the day
        then will validate than can select the item using the user timezone configuration
        Args:
            data: validated data
        Returns:
            validated data
        """
        data = super().validate(data)
        select = MenuSelectByUser.objects.filter(user=data["user"], menu=data["menu"])
        if select.exists():
            raise serializers.ValidationError("You have already selected this menu")
        if not can_user_select_lunch(
            timezone_data=self.timezone_data, menu=data["menu"]
        ):
            raise serializers.ValidationError("You can't select lunch")
        return data


class MenuSelectByUserReadSerializer(serializers.ModelSerializer):

    user = UserSerializer()

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
