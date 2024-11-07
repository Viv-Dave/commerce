# Generated by Django 5.1.3 on 2024-11-06 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_remove_listing_end_date_remove_listing_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='updated_price',
        ),
        migrations.AddField(
            model_name='listing',
            name='photo_url',
            field=models.ImageField(default='abcd.jpg', upload_to='Product_Images'),
        ),
    ]