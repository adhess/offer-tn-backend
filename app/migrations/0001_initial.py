# Generated by Django 3.1.3 on 2020-11-22 19:33

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='app.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ref', models.CharField(max_length=255)),
                ('characteristics', models.JSONField()),
                ('popularity', models.IntegerField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='ScrapyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('age', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('website', models.CharField(max_length=255)),
                ('logo_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='StartUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_urls', to='app.category')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.scrapyitem')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_urls', to='app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVendorDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('unit_price', models.FloatField()),
                ('discount_available', models.BooleanField(default=False)),
                ('warranty', models.CharField(max_length=50)),
                ('inventory_state', models.CharField(choices=[('IS', 'In stock'), ('OOS', 'Out of stock'), ('IT', 'In transit'), ('OC', 'On command')], default='IS', max_length=5)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='app.product')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.URLField()),
                ('product_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app.productvendordetails')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='one_image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image_product', to='app.productimage'),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('characteristics', models.JSONField()),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='app.category')),
            ],
        ),
    ]
