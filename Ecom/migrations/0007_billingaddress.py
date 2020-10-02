# Generated by Django 3.1.1 on 2020-10-02 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ecom', '0006_orderitem_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(blank=True, max_length=100, null=True)),
                ('appartment_address', models.CharField(blank=True, max_length=100, null=True)),
                ('countries', django_countries.fields.CountryField(max_length=2)),
                ('zipcode', models.CharField(max_length=100)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]