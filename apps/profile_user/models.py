from django.db import models


class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    location = models.ForeignKey(
        "location.Country", on_delete=models.CASCADE, null=True, blank=True
    )
    slack_user = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"UserProfile: {self.user.username}"
