# Generated by Django 4.2.3 on 2023-08-16 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Companion', '0009_alter_companion_scraped_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companion',
            name='city',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='companion',
            name='continent',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='companion',
            name='country',
            field=models.CharField(max_length=30),
        ),
    ]
