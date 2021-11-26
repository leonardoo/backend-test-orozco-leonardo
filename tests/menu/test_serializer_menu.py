import pytest

from apps.menu.api.serializers.menu import MenuSerializer
from apps.menu.models import Menu, MenuItem


@pytest.mark.django_db
def test_serializer_menu_with_items(create_location):
    data = {
        "day": "2021-11-23",
        "name": "Test menu",
        "location": create_location[1].id,
        "items": [
            {
                "dishes": [
                    {
                        "name": "Test item",
                    }
                ]
            }
        ],
    }
    serializer = MenuSerializer(data=data)
    is_valid = serializer.is_valid()
    assert is_valid is True


@pytest.mark.django_db
def test_serializer_menu_with_items_empty(create_location):
    data = {
        "day": "2021-11-23",
        "name": "Test menu",
        "location": create_location[1].id,
        "items": [],
    }
    serializer = MenuSerializer(data=data)
    is_valid = serializer.is_valid()
    assert is_valid is False


@pytest.mark.django_db
def test_serializer_menu_with_items_dishes_empty(create_location):
    data = {
        "day": "2021-11-23",
        "name": "Test menu",
        "location": create_location[1].id,
        "items": [
            {
                "dishes": [
                    {
                        "name": "Test item",
                    },
                    {
                        "name": "",
                    },
                ]
            }
        ],
    }
    serializer = MenuSerializer(data=data)
    is_valid = serializer.is_valid()
    assert is_valid is False


@pytest.mark.django_db
def test_serializer_menu_perform_create(create_location):
    data = {
        "day": "2021-11-23",
        "name": "Test menu",
        "location": create_location[1].id,
        "items": [
            {
                "dishes": [
                    {
                        "name": "Test item",
                    },
                    {
                        "name": "Item 2",
                    },
                ]
            }
        ],
    }
    serializer = MenuSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    assert serializer.data["id"] is not None
    assert Menu.objects.count() == 1
    assert MenuItem.objects.count() == 1
