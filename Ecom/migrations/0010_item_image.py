# Generated by Django 3.1.1 on 2020-10-03 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0009_auto_20201002_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='img/default.jpg', null=True, upload_to='img/item_images'),
        ),
    ]
