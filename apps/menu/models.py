import json
import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from apps.menu.constants import MenuStatus


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.DateField()
    status = models.CharField(
        choices=MenuStatus.choices, max_length=20, default=MenuStatus.ACTIVE
    )
    location = models.ForeignKey("location.Country", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{_('Menu for')} {self.day.isoformat()}"

    class Meta:
        unique_together = ("day", "location")

    def get_absolute_url(self):
        return reverse_lazy("menu:menu_detail", kwargs={"pk": self.pk})


class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    dishes = JSONField(null=True)
    created_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_json_as_str(self):
        return json.dumps(self.dishes or [])


class MenuSelectByUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    comments = JSONField(null=True)

    def get_json_as_str(self):
        return json.dumps(self.comments or [])
