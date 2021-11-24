from django.urls import include, path

from apps.location.views import (
    CountryCreateView,
    CountryDeleteView,
    CountryListView,
    CountryUpdateView,
)

country_urlpatterns = [
    path("", CountryListView.as_view(), name="country_list"),
    path("create/", CountryCreateView.as_view(), name="country_create"),
    path("<int:pk>/edit/", CountryUpdateView.as_view(), name="country_edit"),
    path("<int:pk>/delete/", CountryDeleteView.as_view(), name="country_delete"),
]

urlpatterns = [
    path("country/", include(country_urlpatterns)),
]
