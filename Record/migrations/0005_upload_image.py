# Generated by Django 4.2.3 on 2023-08-13 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Record', '0004_remove_record_scrap_card_card_scrap_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=300)),
            ],
        ),
    ]
