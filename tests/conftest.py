from datetime import date, datetime

import pytest
from django.contrib.auth.models import User
from django.core.cache import cache

from pytz import timezone

from apps.location.models import Country
from apps.menu.models import Menu, MenuItem
from apps.profile_user.models import Profile


@pytest.fixture(autouse=True)
def clean_cache():
    yield
    cache.clear()


@pytest.fixture
def create_location():
    yield Country.objects.bulk_create(
        [
            Country(name="Colombia", tz="America/Bogota"),
            Country(name="Chile", tz="America/Santiago"),
        ]
    )


@pytest.fixture
def create_user(create_location, faker):
    def get_user(is_staff=False, create_profile=True, location=create_location[1]):
        user = User.objects.create(
            username=faker.user_name(),
            first_name="John",
            last_name="Lennon",
            is_staff=is_staff,
        )
        if create_profile:
            Profile.objects.create(user=user, location=location)
        return user

    return get_user


@pytest.fixture
def create_menu(create_location):
    def create_menu_date(day=date.today(), country=create_location[1]):
        menu_items = [
            [
                {
                    "name": "Chicken",
                },
                {
                    "name": "Salad",
                },
            ],
            [
                {
                    "name": "Meat",
                },
                {
                    "name": "Salad",
                },
            ],
            [
                {
                    "name": "vegetarian",
                },
                {
                    "name": "Salad",
                },
            ],
        ]
        menu = Menu.objects.create(
            day=day,
            location=country,
        )
        MenuItem.objects.bulk_create(
            [MenuItem(dishes=item, menu=menu) for item in menu_items]
        )
        return menu

    return create_menu_date


@pytest.fixture
def set_date_lunch(mocker):
    def get_date_user_lunch(day=date.today(), hour=10):
        date_user_lunch = datetime(
            year=day.year,
            month=day.month,
            day=day.day,
            hour=hour,
            minute=0,
            second=0,
            microsecond=0,
        )
        date_user_lunch = timezone("america/santiago").localize(date_user_lunch)
        mocker.patch(
            # api_call is from slow.py but imported to main.py
            "apps.menu.business.get_current_datetime_to_tz",
            return_value=date_user_lunch,
        )

    return get_date_user_lunch
