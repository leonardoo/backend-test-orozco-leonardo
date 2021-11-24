from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


class StaffOnlyMixin(LoginRequiredMixin):
    """
    Mixin class to restrict access to users who are staff.
    """
    def dispatch(self, request, *args, **kwargs):
        dispatch = super().dispatch(request, *args, **kwargs)
        if not request.user.is_staff:
            return HttpResponse('You must be a staff member to view this page.', status=403)
        return dispatch