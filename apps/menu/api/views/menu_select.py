from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from apps.menu.api.serializers.menu_select import MenuSelectByUserSerializer


class MenuSelectCreateViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = MenuSelectByUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, data, *args, **kwargs):
        data["user"] = self.request.user.id
        serializer = super().get_serializer(data=data, *args, **kwargs)
        serializer.timezone_data = self.request.user_timezone_data
        return serializer
