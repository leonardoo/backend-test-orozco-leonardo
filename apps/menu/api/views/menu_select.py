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
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )


class AllowUserToCreate(permissions.IsAuthenticated):
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
        if self.request.method == "GET":
            return MenuSelectByUserReadSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
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
