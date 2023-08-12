# Generated by Django 4.2.3 on 2023-08-11 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Discussion', '0002_alter_dcomment_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='voted_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
