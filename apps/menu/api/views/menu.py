from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission

from django_filters import rest_framework as filters

from apps.menu.api.serializers.menu import MenuItemSerializer, MenuSerializer
from apps.menu.models import Menu, MenuItem


class IsAdminUserOrReadOnly(BasePermission):
    """
    The request is authenticated as a user and is staff, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("menu",)
