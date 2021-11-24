from django.urls import path
from django.views.generic import TemplateView

from .views import (
    view, user_create_view, UserListView, user_edit_profile_view
)

urlpatterns = [
    path("home", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("list/", UserListView.as_view(), name="user_list"),
    path(
        "<str:user>", TemplateView.as_view(template_name="pages/home.html"), name="home"
    ),
    path(
        "create/", user_create_view, name="user_create"
    ),
    path(
        "<int:pk>/edit/", user_edit_profile_view, name="user_profile_edit"
    )
]
