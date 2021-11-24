from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from apps.base.mixins import StaffOnlyMixin
from apps.profile_user.forms import UserProfileForm
from apps.profile_user.models import Profile


@login_required
def view(request):
    return render(request, "pages/test_vue.html")


class UserListView(StaffOnlyMixin, ListView):
    model = User
    queryset = User.objects.prefetch_related("profile", "profile__location").all()
    template_name = "profile/user_list.html"

    def get_context_data(self):
        context = super().get_context_data()
        print(context)
        return context


@login_required
def user_create_view(request):
    if not request.user.is_staff:
        raise PermissionDenied
    status = 200
    form_user = UserCreationForm(request.POST or None, prefix="user")
    form_profile = UserProfileForm(request.POST or None, prefix="profile")
    if form_user.is_valid() and form_profile.is_valid():
        user = form_user.save()
        profile = form_profile.save(commit=False)
        profile.user = user
        profile.save()
        messages.add_message(request, messages.INFO, f'User {user.username} was successfully created')
        status = 201
    return render(request, "profile/user_form.html", {"forms": [form_user, form_profile]}, status=status)


@login_required
def user_edit_profile_view(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    user = get_object_or_404(User.objects.prefetch_related("profile"), pk=pk)
    profile = user.profile if hasattr(user, "profile") else Profile(user_id=pk)
    form_profile = UserProfileForm(request.POST, prefix="profile", instance=profile)
    if form_profile.is_valid():
        form_profile.save()
        messages.add_message(request, messages.INFO, f'User {user.username} was successfully updated profile')
    return render(request, "profile/user_form.html", {"forms": [form_profile]})
