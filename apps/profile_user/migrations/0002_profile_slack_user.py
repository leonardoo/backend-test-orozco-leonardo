# Generated by Django 3.0.8 on 2021-11-23 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slack_user',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
