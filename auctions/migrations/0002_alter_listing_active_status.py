# Generated by Django 5.1.3 on 2024-11-09 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='active_status',
            field=models.BooleanField(default=True),
        ),
    ]
