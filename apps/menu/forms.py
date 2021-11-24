from django import forms

from apps.menu.models import Menu, MenuItem


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["day", "status"]
        widgets = {
            "day": forms.DateInput(attrs={"type": "date"}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["menu", "dishes"]
