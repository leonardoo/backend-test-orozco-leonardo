from rest_framework import mixins, permissions, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django_filters import rest_framework as filters

from apps.menu.api.serializers.menu_select import (
    MenuSelectByUserReadSerializer,
    MenuSelectByUserSerializer,
)
from apps.menu.models import MenuSelectByUser


class IsAdminUser(BasePermission):
    """
    The request is authenticated as a user and is staff.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )


class AllowUserToCreate(permissions.IsAuthenticated):
    """
    The request is authenticated as a user and its post request.
    """

    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) and request.method == "POST")


class MenuSelectCreateViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = MenuSelectByUserSerializer
    permission_classes = [IsAdminUser | AllowUserToCreate]
    queryset = MenuSelectByUser.objects.select_related("user").all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("menu",)

    def get_serializer_class(self):
        """
        Check if the method is a Get and will return the serializer for read information else will return a serializer for create.
        """
        if self.request.method == "GET":
            return MenuSelectByUserReadSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """
        Try to create the menu selected by the user, it will enforce and add the user to the data send in the requests,
        and also will add the user_timezone_data
        Returns:
            object: Response
        """
        data = request.data
        data["user"] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.timezone_data = self.request.user_timezone_data
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
