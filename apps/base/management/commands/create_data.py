from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.location.models import Country


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("username", nargs="?", type=str, default="nora")
        parser.add_argument("slack_channel_id", nargs="+", type=str, default=None)

    def handle(self, *args, **options):
        """
        Creates a user and a country so can start to use the app
        """
        username = options["username"]
        slack_channel_id = options["slack_channel_id"][0]
        if user := User.objects.filter(username=username).first():
            self.stdout.write(
                self.style.SUCCESS(f"User {user.username} already exists")
            )
        else:
            user = User.objects.create_user(username, "123456", is_staff=True)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user {user.username}")
            )
        if not Country.objects.filter(name="Chile").exists():
            country = Country.objects.create(
                name="Chile", tz="america/santiago", slack_channel_id=slack_channel_id
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully Location {country.name}")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Location Chile already exists"))
