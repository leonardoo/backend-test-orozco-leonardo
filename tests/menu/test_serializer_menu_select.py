import pytest

from apps.menu.api.serializers.menu_select import MenuSelectByUserSerializer
from apps.menu.models import MenuItem


@pytest.mark.django_db
def test_serializer_menu_select_valid(create_menu, create_user, create_location, set_date_lunch):
    menu = create_menu()
    user = create_user()
    set_date_lunch()
    data = {
        "menu": menu.id,
        "user": user.id,
        "item": MenuItem.objects.first().id,
        "comments": ["test"]
    }
    location = create_location[1]
    serializer = MenuSelectByUserSerializer(data=data)
    serializer.timezone_data = {"location": menu.location_id, "timezone": location.tz}
    is_valid = serializer.is_valid()
    assert is_valid is True


@pytest.mark.django_db
def test_serializer_menu_select_invalid(create_menu, create_user, create_location, set_date_lunch):
    menu = create_menu()
    user = create_user()
    set_date_lunch(hour=23)
    data = {
        "menu": menu.id,
        "user": user.id,
        "item": MenuItem.objects.first().id,
        "comments": ["test"]
    }
    location = create_location[1]
    serializer = MenuSelectByUserSerializer(data=data)
    serializer.timezone_data = {"location": menu.location_id, "timezone": location.tz}
    is_valid = serializer.is_valid()
    assert is_valid is False
