from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0014_auto_20210209_0946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='Category',
            old_name='isActive',
            new_name='is_active'),
        migrations.RenameField(
            model_name='Product',
            old_name='ref',
            new_name='reference'),
        migrations.RenameField(
            model_name='ProductVendorDetails',
            old_name='product_url',
            new_name='link_in_vendor_website'),
        migrations.RenameField(
            model_name='ProductVendorDetails',
            old_name='discount_available',
            new_name='is_discount_available'),

    ]
