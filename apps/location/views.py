from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.base.mixins import StaffOnlyMixin
from apps.location.forms import CountryForm
from apps.location.models import Country


class CountryCreateView(StaffOnlyMixin, CreateView):
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy("location:country_list")
    template_name = "base_form.html"


class CountryUpdateView(StaffOnlyMixin, UpdateView):
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy("location:country_list")
    template_name = "base_form.html"


class CountryDeleteView(StaffOnlyMixin,DeleteView):
    model = Country
    success_url = reverse_lazy("location:country_list")


class CountryListView(StaffOnlyMixin, ListView):
    model = Country
    context_object_name = "countries"
    paginate_by = 10
