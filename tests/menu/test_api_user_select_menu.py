import json

import pytest

from apps.menu.models import MenuItem, MenuSelectByUser


@pytest.mark.django_db
def test_user_select_menu(client, create_user, create_menu, set_date_lunch):
    set_date_lunch()
    menu = create_menu()
    user = create_user()
    client.force_login(user)
    data = {
        "menu": str(menu.id),
        "user": user.id,
        "item": str(MenuItem.objects.first().id),
        "comments": "sin cebolla",
    }
    response = client.post(
        "/api/v1/menu_select/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert MenuSelectByUser.objects.count() == 1


@pytest.mark.django_db
def test_user_select_menu_dont_let_select_twice(
    client, create_user, create_menu, set_date_lunch
):
    set_date_lunch()
    menu = create_menu()
    user = create_user()
    client.force_login(user)
    MenuSelectByUser.objects.create(
        menu=menu, user=user, item=MenuItem.objects.first(), comments="sin cebolla"
    )
    data = {
        "menu": str(menu.id),
        "user": user.id,
        "item": str(MenuItem.objects.last().id),
        "comments": "sin cebolla",
    }
    response = client.post(
        "/api/v1/menu_select/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400
    assert MenuSelectByUser.objects.count() == 1


@pytest.mark.django_db
def test_user_select_menu_after_require_hour(
    client, create_user, create_menu, set_date_lunch
):
    set_date_lunch(hour=11)
    menu = create_menu()
    user = create_user()
    client.force_login(user)
    data = {
        "menu": str(menu.id),
        "user": user.id,
        "item": str(MenuItem.objects.last().id),
        "comments": "sin cebolla",
    }
    response = client.post(
        "/api/v1/menu_select/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400
    assert MenuSelectByUser.objects.count() == 0
