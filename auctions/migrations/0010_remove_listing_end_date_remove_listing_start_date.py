# Generated by Django 5.1.2 on 2024-11-05 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bid_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='start_date',
        ),
    ]
