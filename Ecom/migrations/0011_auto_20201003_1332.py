# Generated by Django 3.1.1 on 2020-10-03 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0010_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='item_images/'),
        ),
    ]
