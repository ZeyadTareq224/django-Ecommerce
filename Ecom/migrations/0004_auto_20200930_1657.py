# Generated by Django 3.1.1 on 2020-09-30 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0003_auto_20200930_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='descount_price',
            new_name='discount_price',
        ),
    ]
