from uuid import uuid4

import pytest

from apps.menu.models import MenuItem


@pytest.mark.django_db
def test_edit_menu_remove_dish(client, create_user, create_menu, create_location):
    user = create_user(is_staff=True)
    menu = create_menu()
    location = create_location[1]
    client.force_login(user)
    items = MenuItem.objects.filter(menu=menu)
    data = {
        "day": menu.day.isoformat(),
        "location": location.id,
        "items": [
            {
                "id": item.id,
                "menu": menu.id,
                "dishes": [
                    {
                        "name": f"Chicken {counter}.1",
                    },
                    {
                        "name": f"Salad {counter}.1",
                    },
                ],
            }
            for counter, item in enumerate(items)
        ],
    }
    data["items"][0]["action"] = "delete"
    # data["items"].append({"dishes": [{"name": 'Last Dish'}]})
    response = client.put(
        f"/api/v1/menu/{menu.id}/", data=data, content_type="application/json"
    )
    assert response.status_code == 200
    assert response.json()["id"] == str(menu.id)
    assert MenuItem.objects.count() == 2


@pytest.mark.django_db
def test_edit_add_to_menu_dish(client, create_user, create_menu, create_location):
    user = create_user(is_staff=True)
    menu = create_menu()
    location = create_location[1]
    client.force_login(user)
    items = MenuItem.objects.filter(menu=menu)
    data = {
        "day": menu.day.isoformat(),
        "location": location.id,
        "items": [
            {
                "id": item.id,
                "menu": menu.id,
                "dishes": [
                    {
                        "name": f"Chicken {counter}.1",
                    },
                    {
                        "name": f"Salad {counter}.1",
                    },
                ],
            }
            for counter, item in enumerate(items)
        ],
    }
    data["items"][0]["action"] = "delete"
    data["items"].append({"menu": menu.id, "dishes": [{"name": "Last Dish"}]})
    data["items"].append({"menu": menu.id, "dishes": [{"name": "Last Dish 2"}]})
    response = client.put(
        f"/api/v1/menu/{menu.id}/", data=data, content_type="application/json"
    )
    assert response.status_code == 200
    assert MenuItem.objects.filter(menu=menu).count() == 4


@pytest.mark.django_db
def test_edit_fail_to_add_menu_dish(client, create_user, create_menu, create_location):
    user = create_user(is_staff=True)
    menu = create_menu()
    location = create_location[1]
    client.force_login(user)
    items = MenuItem.objects.filter(menu=menu)
    data = {
        "day": menu.day.isoformat(),
        "location": location.id,
        "items": [
            {
                "id": uuid4(),
                "menu": menu.id,
                "dishes": [
                    {
                        "name": f"Chicken {counter}.1",
                    },
                    {
                        "name": f"Salad {counter}.1",
                    },
                ],
            }
            for counter, item in enumerate(items)
        ],
    }
    data["items"][0]["action"] = "delete"
    data["items"].append({"dishes": [{"name": "Last Dish"}]})
    data["items"].append({"dishes": [{"name": "Last Dish 2"}]})
    response = client.put(
        f"/api/v1/menu/{menu.id}/", data=data, content_type="application/json"
    )
    assert response.status_code == 400
