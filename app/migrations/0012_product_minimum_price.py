# Generated by Django 3.1.2 on 2020-12-12 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20201208_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='minimum_price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=12),
            preserve_default=False,
        ),
    ]
