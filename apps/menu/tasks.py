import logging

from celery import task
from django.conf import settings

from slack.errors import SlackApiError
from slack.web.client import WebClient

from apps.location.models import Country
from apps.menu.business import get_current_datetime_to_tz
from apps.menu.constants import MenuStatus
from apps.menu.models import Menu

logger = logging.getLogger(__name__)


@task
def send_menu_to_slack(menu_id: str, resend: bool = False):
    """
    Get a menu and send it to slack
    """
    menu = Menu.objects.select_related("location").get(id=menu_id)
    if menu.status == MenuStatus.SEND and not resend:
        return
    if not menu.location.slack_channel_id:
        return
    client = WebClient(token=settings.SLACK_TOKEN)
    try:
        client.conversations_join(channel=menu.location.slack_channel_id)
        data = {
            "fields": [
                {
                    "value": f"<{settings.SITE_URL}{menu.get_absolute_url()}|Menu>",
                    "short": False,
                }
            ]
        }
        client.chat_postMessage(
            channel=menu.location.slack_channel_id,
            text=f"the menu for {menu.day.isoformat()}",
            attachments=[data],
        )
        if menu.status == MenuStatus.SEND:
            menu.status = MenuStatus.RESEND
        else:
            menu.status = MenuStatus.SEND
        menu.save()
    except SlackApiError:
        logging.exception(f"An Error occurred when trying to send menu {menu_id}")


@task
def select_menu_to_send_auto():
    """
    Selects the menu to send automatically, using the country's timezone
    """
    countries = (
        Country.objects.filter(slack_channel_id__isnull=False)
        .exclude(slack_channel_id="")
        .all()
    )
    for country in countries:
        date_time = get_current_datetime_to_tz({"timezone": country.tz.zone})
        if date_time.hour > settings.SLACK_SEND_MENU_HOUR:
            continue
        menus = Menu.objects.filter(location=country).exclude(
            status__in=[MenuStatus.SEND, MenuStatus.RESEND]
        )
        menus = menus.filter(day=date_time.date())
        for menu in menus:
            send_menu_to_slack.delay(str(menu.id))
