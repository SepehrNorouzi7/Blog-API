# Generated by Django 4.2.16 on 2024-09-21 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
    ]
