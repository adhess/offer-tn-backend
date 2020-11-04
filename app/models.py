from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class Vendor(models.Model):
    name = models.CharField(max_length=50)
    website = models.CharField(max_length=255)


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='children')


class Product(models.Model):
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=255)
    characteristics = models.JSONField()
    popularity = models.IntegerField(null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='products')
    one_image = models.OneToOneField("ProductImage", on_delete=models.CASCADE, related_name='image_product')


class Filter(models.Model):
    characteristics = models.JSONField()
    # characteristics = {cpu: "checkbox"}
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='filters')


class ProductVendorDetails(models.Model):

    class InventoryState(models.TextChoices):
        IN_STOCK = 'IS', _('In stock')
        OUT_OF_STOCK = 'OOS', _('Out of stock')
        IN_TRANSIT = 'IT', _('In transit')
        ON_COMMAND = 'OC', _('On command')

    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_from_all_vendors")
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name="products")
    url = models.URLField()
    unit_price = models.FloatField()
    discount_available = models.BooleanField(default=False)
    warranty = models.CharField(max_length=50)
    inventory_state = models.CharField(
        max_length=5,
        choices=InventoryState.choices,
        default=InventoryState.IN_STOCK,
    )


class ProductImage(models.Model):
    src = models.URLField()
    product = models.ForeignKey('ProductVendorDetails', on_delete=models.CASCADE, related_name='images')
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name='images')


class StartUrl(models.Model):
    url = models.URLField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='start_urls')
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name='start_urls')


