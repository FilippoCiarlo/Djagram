# Generated by Django 4.1 on 2023-01-21 17:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0003_alter_followers_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="follows",
            field=models.ManyToManyField(
                related_name="follows", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
