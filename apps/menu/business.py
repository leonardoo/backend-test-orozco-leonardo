from datetime import datetime

from django.conf import settings

import pytz
from pytz import timezone


def get_current_datetime_to_tz(timezone_data):
    return datetime.now(tz=timezone(timezone_data["timezone"]))


def can_user_select_lunch(timezone_data, menu):
    date_until_lunch = datetime(
        year=menu.day.year,
        month=menu.day.month,
        day=menu.day.day,
        hour=settings.SLACK_SEND_MENU_HOUR,
        minute=0,
        second=0,
        microsecond=0,
    )
    tz = timezone(
        menu.location.tz.zone if menu.location and menu.location.tz else pytz.UTC.zone
    )
    date_until_lunch = tz.localize(date_until_lunch)
    return (
        timezone_data["location"] == menu.location_id
        and get_current_datetime_to_tz(timezone_data) < date_until_lunch
    )
