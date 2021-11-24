from django import forms

from apps.location.models import Country


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ["name", "tz"]
