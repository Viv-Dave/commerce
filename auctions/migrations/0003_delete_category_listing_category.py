# Generated by Django 5.1.2 on 2024-11-05 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(default='General', max_length=64),
        ),
    ]
