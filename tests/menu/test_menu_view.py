import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_menu_detail_is_view_as_read_only_with_user(client, create_menu):
    menu = create_menu()
    url = reverse("menu:menu_detail", kwargs={"pk": menu.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["read_only_mode"] is True


@pytest.mark.django_db
def test_menu_detail_is_view_as_read_only_with_user_from_another_location(
    client, create_menu, create_user, create_location
):
    col = create_location[0]
    menu = create_menu(country=col)
    user = create_user(create_profile=True)
    url = reverse("menu:menu_detail", kwargs={"pk": menu.pk})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["read_only_mode"] is True


@pytest.mark.django_db
def test_menu_detail_view_for_send_lunch(
    client, create_menu, create_user, set_date_lunch
):
    set_date_lunch()
    menu = create_menu()
    user = create_user(create_profile=True)
    url = reverse("menu:menu_detail", kwargs={"pk": menu.pk})
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 200
    assert response.context["read_only_mode"] is False


@pytest.mark.django_db
def test_menu_create_view(
    client, create_menu, create_user, set_date_lunch
):
    set_date_lunch()
    user = create_user(create_profile=True)
    url = reverse("menu:menu_create")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_menu_create_view(
    client, create_menu, create_user, set_date_lunch
):
    set_date_lunch()
    user = create_user(create_profile=True)
    url = reverse("menu:menu_create")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403



