from django.db import models

from timezone_field import TimeZoneField


class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)
    tz = TimeZoneField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
