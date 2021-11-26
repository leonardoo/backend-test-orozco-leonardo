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


@pytest.mark.django_db
def test_user_select_menu_dont_allow_get_api(
    client, create_user, create_menu, set_date_lunch
):
    menu = create_menu()
    user = create_user()
    client.force_login(user)
    selected = MenuSelectByUser.objects.create(
        menu=menu, user=user, item=MenuItem.objects.first(), comments="sin cebolla"
    )
    response = client.get(
        f"/api/v1/menu_select/{selected.id}/", content_type="application/json"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_select_menu_get_api(client, create_user, create_menu, set_date_lunch):
    menu = create_menu()
    user = create_user(is_staff=True)
    client.force_login(user)
    selected = MenuSelectByUser.objects.create(
        menu=menu, user=user, item=MenuItem.objects.first(), comments="sin cebolla"
    )
    response = client.get(
        f"/api/v1/menu_select/{selected.id}/", content_type="application/json"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_select_menu_filter_by_menu(
    client, create_user, create_menu, create_location
):
    menu = create_menu()
    user = create_user(is_staff=True)
    for _ in range(2):
        MenuSelectByUser.objects.create(
            menu=menu,
            user=create_user(),
            item=MenuItem.objects.first(),
            comments="without onion",
        )
    other_menu = create_menu(country=create_location[0])
    for _ in range(3):
        MenuSelectByUser.objects.create(
            menu=other_menu,
            user=create_user(),
            item=MenuItem.objects.first(),
            comments="without onion",
        )
    client.force_login(user)
    response = client.get(
        f"/api/v1/menu_select/?menu={menu.id}", content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 2
