import pytest
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from apps.profile_user.models import Profile


@pytest.mark.django_db
def test_get_profile_list(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.get(reverse_lazy('profile:user_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_dont_allow_to_view_profile_list_user_not_staff(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=False)
    client.force_login(user)
    response = client.get(reverse_lazy('profile:user_list'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_profile_create_get(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.get(reverse_lazy('profile:user_create'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_dont_allow_user_not_staff_to_get_create_user_profile(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user()
    client.force_login(user)
    response = client.get(reverse_lazy('profile:user_create'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_profile_edit_get(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.get(reverse_lazy('profile:user_profile_edit', kwargs={'pk': user.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_dont_allow_user_not_staff_to_get_edit_user_profile(client, create_user):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user()
    client.force_login(user)
    response = client.get(reverse_lazy('profile:user_profile_edit', kwargs={'pk': user.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_profile_create_post(client, create_user, create_location):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.post(reverse_lazy('profile:user_create'), data={
        "user-username": "test_user",
        "user-password1": "very_simple_test",
        "user-password2": "very_simple_test",
        "profile-location": create_location[0].id
    })
    assert response.status_code == 201
    assert Profile.objects.count() == 2
    assert User.objects.count() == 2
    user_new = User.objects.prefetch_related("profile").exclude(pk=user.pk).first()
    assert user_new.username == "test_user"
    assert user_new.profile.location_id == create_location[0].pk


@pytest.mark.django_db
def test_user_profile_edit_post(client, create_user, create_location):
    """
    GIVEN a Flask application
    WHEN the '/profile/create' page is requested
    THEN check the response is valid
    """
    user = create_user(is_staff=True)
    client.force_login(user)
    response = client.post(reverse_lazy('profile:user_profile_edit', kwargs={"pk": user.pk}), data={
        "profile-location": create_location[0].id,
        "profile-slack_user": "user_slack_test"
    })
    assert response.status_code == 200
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1
    user.refresh_from_db()
    assert user.profile.location_id == create_location[0].pk
    assert user.profile.slack_user == "user_slack_test"

