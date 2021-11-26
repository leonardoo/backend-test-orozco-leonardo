import datetime
import json

import pytest

from apps.menu.constants import MenuStatus
from apps.menu.models import Menu, MenuItem


@pytest.mark.django_db
def test_create_menu_by_api(client, create_user, create_location):

    user = create_user(is_staff=True)
    location = create_location[1]
    client.force_login(user)
    data = {
        "day": datetime.date.today().isoformat(),
        "status": MenuStatus.ACTIVE,
        "location": location.id,
        "items": [
            {
                "dishes": [{"name": "Dish 1"}, {"name": "Dish 2"}],
            },
            {
                "dishes": [{"name": "Dish 3"}, {"name": "Dish 4"}],
            },
        ],
    }
    response = client.post(
        "/api/v1/menu/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert Menu.objects.count() == 1
    assert MenuItem.objects.count() == 2


@pytest.mark.django_db
def test_create_menu_by_api_items_empty(client, create_user):

    user = create_user(is_staff=True)
    client.force_login(user)
    data = {
        "day": datetime.date.today().isoformat(),
        "status": MenuStatus.ACTIVE,
        "items": [],
    }
    response = client.post(
        "/api/v1/menu/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400
    assert Menu.objects.count() == 0
    assert MenuItem.objects.count() == 0
