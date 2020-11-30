# Generated by Django 3.1.3 on 2020-11-28 16:18

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_productvendordetails_unit_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvendordetails',
            name='registered_prices',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=3, max_digits=12), size=None),
        ),
        migrations.AddField(
            model_name='productvendordetails',
            name='registered_prices',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.DecimalField(decimal_places=3, max_digits=12), size=None),
        ),

    ]