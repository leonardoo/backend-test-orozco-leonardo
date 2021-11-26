from datetime import date, datetime

import pytest
from django.conf import settings

from pytz import timezone

from apps.menu.constants import MenuStatus
from apps.menu.tasks import select_menu_to_send_auto, send_menu_to_slack


@pytest.fixture
def slack_client(mocker):

    return mocker.patch(
        "apps.menu.tasks.WebClient",
        return_value=mocker.Mock(
            **{
                "conversations_join.return_value": None,
                "chat_postMessage.return_value": None,
            }
        ),
    )


@pytest.fixture
def send_menu_slack_mock(mocker):
    return mocker.patch("apps.menu.tasks.send_menu_to_slack.delay", return_value=None)


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
            "apps.menu.tasks.get_current_datetime_to_tz",
            return_value=date_user_lunch,
        )

    return get_date_user_lunch


@pytest.mark.django_db
def test_send_msg_to_slack(create_menu, slack_client):
    menu = create_menu()
    send_menu_to_slack(str(menu.id))
    slack_client.assert_called_once()
    slack_client().conversations_join.assert_called_once()
    slack_client().chat_postMessage.assert_called_once()
    args = slack_client().chat_postMessage.call_args
    assert args[1]["text"] == f"the menu for {menu.day.isoformat()}"
    assert (
        f"{settings.SITE_URL}{menu.get_absolute_url()}"
        in args[1]["attachments"][0]["fields"][0]["value"]
    )
    menu.refresh_from_db()
    assert menu.status == MenuStatus.SEND


@pytest.mark.django_db
def test_send_msg_to_slack_call_twice(create_menu, slack_client):
    menu = create_menu()
    send_menu_to_slack(str(menu.id))
    send_menu_to_slack(str(menu.id))
    slack_client.assert_called_once()
    slack_client().conversations_join.assert_called_once()
    slack_client().chat_postMessage.assert_called_once()
    menu.refresh_from_db()
    assert menu.status == MenuStatus.SEND


@pytest.mark.django_db
def test_send_msg_to_slack_call_twice_with_resend(create_menu, slack_client):
    menu = create_menu()
    send_menu_to_slack(str(menu.id))
    send_menu_to_slack(str(menu.id), resend=True)
    assert slack_client.call_count == 2
    assert slack_client().conversations_join.call_count == 2
    assert slack_client().chat_postMessage.call_count == 2
    menu.refresh_from_db()
    assert menu.status == MenuStatus.RESEND


@pytest.mark.django_db
def test_send_msg_to_send_menu_slack(
    create_menu, create_location, send_menu_slack_mock, set_date_lunch
):
    set_date_lunch(hour=10)
    create_menu()
    select_menu_to_send_auto()
    send_menu_slack_mock.assert_called_once()
