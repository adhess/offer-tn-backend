# Generated by Django 3.1.2 on 2020-11-20 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201105_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='one_image',
        ),
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='min_registered_prices',
            field=models.JSONField(default={'data': []}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productvendordetails',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='app.product'),
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]