from django.core.cache import cache

import pytz

from apps.profile_user.constants import USER_CACHE_TIMEZONE_KEY
from apps.profile_user.models import Profile


class AddUserProfileMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Add the user Timezone location to the request, if it exists.
        with thisdwe can check if the user its in the same timezone of the menu that is being requested.
        :param request:
        :return: (response)
        """
        if request.user.is_authenticated:
            timezone_data = cache.get(USER_CACHE_TIMEZONE_KEY.format(request.user.id))
            if not timezone_data:
                profile = (
                    Profile.objects.select_related("location")
                    .filter(user=request.user)
                    .first()
                )
                timezone_data = {"timezone": pytz.UTC.zone, "location": ""}
                if profile and profile.location:
                    timezone_data = {
                        "timezone": profile.location.tz.zone,
                        "location": profile.location_id,
                    }
                    cache.set(
                        USER_CACHE_TIMEZONE_KEY.format(request.user.id),
                        timezone_data,
                        None,
                    )
            request.user_timezone_data = timezone_data
        return self.get_response(request)
