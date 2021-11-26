# Generated by Django 3.0.8 on 2021-11-25 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("location", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="country",
            options={"ordering": ["id"]},
        ),
        migrations.AddField(
            model_name="country",
            name="slack_channel_id",
            field=models.CharField(blank=True, default="", max_length=30),
        ),
    ]