import pytest

from apps.location.forms import CountryForm
from apps.location.models import Country


@pytest.mark.django_db
def test_form_create_country():
    form = CountryForm(data={"name": "Test Country", "tz": "America/Bogota"})
    assert form.is_valid()
    form.save()
    assert Country.objects.count() == 1
    country = Country.objects.first()
    assert country.name == "Test Country"
    assert country.tz.zone == "America/Bogota"


@pytest.mark.django_db
def test_form_invalid_timezone():
    form = CountryForm(data={"name": "Test Country", "tz": ""})
    assert form.is_valid() is False


@pytest.mark.django_db
def test_form_dont_allow_create_another_with_same_name(create_location):
    location = create_location[1]
    form = CountryForm(data={"name": location.name, "tz": "America/Bogota"})
    assert form.is_valid() is False
