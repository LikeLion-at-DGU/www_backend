# Generated by Django 4.2.3 on 2023-08-14 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="city",
        ),
        migrations.RemoveField(
            model_name="user",
            name="country",
        ),
        migrations.RemoveField(
            model_name="user",
            name="nickname",
        ),
    ]