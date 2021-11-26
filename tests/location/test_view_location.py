import pytest
from django.urls import reverse_lazy

from apps.location.models import Country


@pytest.mark.django_db
def test_get_location_list(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.get(reverse_lazy("location:country_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_location_list_with_data(client, create_user, create_location):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.get(reverse_lazy("location:country_list"))
    assert response.status_code == 200
    assert response.context["object_list"].count() == 2


@pytest.mark.django_db
def test_dont_allow_to_view_location_list_user_not_staff(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=False)
    client.force_login(user)
    response = client.get(reverse_lazy("location:country_list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_location_create_get(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.get(reverse_lazy("location:country_create"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_dont_allow_user_not_staff_to_get_create_location(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user()
    client.force_login(user)
    response = client.get(reverse_lazy("location:country_create"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_location_edit_get(client, create_user, create_location):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    location = create_location[0]
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.get(
        reverse_lazy("location:country_edit", kwargs={"pk": location.pk})
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_dont_allow_user_not_staff_to_get_edit_location(
    client, create_user, create_location
):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    location = create_location[0]
    user = create_user()
    client.force_login(user)
    response = client.get(
        reverse_lazy("location:country_edit", kwargs={"pk": location.pk})
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_location_create_post(client, create_user, create_location):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.post(
        reverse_lazy("location:country_create"),
        data={"name": "Test Country", "tz": "America/Bogota"},
        follow=True,
    )
    assert response.status_code == 200
    assert (
        Country.objects.exclude(
            pk__in=[location.pk for location in create_location]
        ).count()
        == 1
    )
    country = Country.objects.exclude(
        pk__in=[location.pk for location in create_location]
    ).first()
    assert country.name == "Test Country"
    assert country.tz.zone == "America/Bogota"


@pytest.mark.django_db
def test_location_edit_post(client, create_user, create_location):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    location = create_location[0]
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.post(
        reverse_lazy("location:country_edit", kwargs={"pk": location.pk}),
        data={"name": "Test Country", "tz": "America/Bogota"},
        follow=True,
    )
    assert response.status_code == 200
    assert Country.objects.count() == 2
    location.refresh_from_db()
    assert location.name == "Test Country"
    assert location.tz.zone == "America/Bogota"
