# Generated by Django 3.1.1 on 2020-10-05 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0021_remove_shippingaddress_payment_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(blank=True, choices=[('Electronics', 'E'), ('Head Wears', 'HW'), ('Foot Wear', 'FW'), ('Development', 'DEV'), ('Head Wears', 'HW'), ('Books & Novels', 'BN'), ('Shirts', 'SH'), ('Sport Wears', 'SW'), ('Out Wears', 'OW')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
