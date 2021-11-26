from django.db import models

from timezone_field import TimeZoneField


class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)
    tz = TimeZoneField()
    slack_channel_id = models.CharField(max_length=30, blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
