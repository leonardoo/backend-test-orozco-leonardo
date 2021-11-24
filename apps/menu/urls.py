from django.urls import path

from .views.menu import (
    MenuCreateView, MenuDetailView, MenuListView, MenuUpdateView, MenuDetailSelectedView
)

urlpatterns = [
    path("create/", MenuCreateView.as_view(), name="menu_create"),
    path("", MenuListView.as_view(), name="menu_list"),
    path("<str:pk>/edit/", MenuUpdateView.as_view(), name="menu_update"),
    path("<str:pk>", MenuDetailView.as_view(), name="menu_detail"),
    path("<str:pk>/selected/", MenuDetailSelectedView.as_view(), name="menu_select_detail"),
]
