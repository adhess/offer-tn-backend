# Generated by Django 3.1.3 on 2020-11-25 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201120_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapyitem',
            name='age',
        ),
    ]