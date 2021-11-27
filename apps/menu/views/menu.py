from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from apps.base.mixins import StaffOnlyMixin
from apps.menu.business import can_user_select_lunch, get_current_datetime_to_tz
from apps.menu.models import Menu, MenuItem, MenuSelectByUser


class MenuCreateView(StaffOnlyMixin, TemplateView):

    template_name = "menu/menu_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timezone_data = self.request.user_timezone_data
        context["day"] = get_current_datetime_to_tz(timezone_data).date().isoformat()
        return context


class MenuListView(ListView, LoginRequiredMixin):
    model = Menu
    context_object_name = "menus"


class MenuUpdateView(MenuCreateView):
    template_name = "menu/menu_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = get_object_or_404(Menu, pk=self.kwargs["pk"])
        context["menu_id"] = self.kwargs["pk"]
        context["day"] = context["menu"].day.isoformat()
        return context


class MenuDetailView(DetailView):
    model = Menu
    context_object_name = "menu"
    queryset = Menu.objects.select_related("location")

    def get_context_data(self, **kwargs):
        """
        Check if the user can select lunch for the day, or  will be only to see it,
        also add the selected dish in the context that the user select for the menu from the day
        Args:
            **kwargs:
        Returns:
            context: with the readonly flag and the
        """
        context = super().get_context_data(**kwargs)
        read_only_mode = True
        context["dish_select"] = None
        if self.request.user.is_authenticated:
            selected_dish = (
                MenuSelectByUser.objects.select_related("item")
                .filter(user=self.request.user, menu=self.object)
                .first()
            )
            context["dish_select"] = selected_dish or {}
        if self.request.user.is_authenticated and not context["dish_select"]:
            timezone_data = self.request.user_timezone_data
            menu = self.object
            read_only_mode = not can_user_select_lunch(timezone_data, menu)
        context["read_only_mode"] = read_only_mode
        context["dishes"] = MenuItem.objects.filter(menu=self.object)
        return context


class MenuDetailSelectedView(StaffOnlyMixin, DetailView):
    model = Menu
    context_object_name = "menu"
    template_name = "menu/menu_detail_user_selection.html"
    queryset = Menu.objects.select_related("location")
