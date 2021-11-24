import pytest

from apps.profile_user.forms import UserProfileForm
from apps.profile_user.models import Profile


@pytest.mark.django_db
def test_create_profile_for_user(create_user, create_location):
    user = create_user(create_profile=False)

    form = UserProfileForm(data={
        'location': create_location[0].id,
        "slack_user": ""
    }, instance=Profile(user=user))

    assert form.is_valid()
    form.save()
    assert Profile.objects.count() == 1
    profile = Profile.objects.first()
    assert profile.user == user
    assert profile.location == create_location[0]


@pytest.mark.django_db
def test_allow_create_profile_for_user_without_location(create_user, create_location):
    user = create_user(create_profile=False)

    form = UserProfileForm(data={
        'location': "",
        "slack_user": ""
    }, instance=Profile(user=user))

    assert form.is_valid()
    form.save()
    assert Profile.objects.count() == 1
    profile = Profile.objects.first()
    assert profile.user == user


