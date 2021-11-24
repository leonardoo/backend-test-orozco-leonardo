from .models import Profile
from django import forms


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'slack_user']

