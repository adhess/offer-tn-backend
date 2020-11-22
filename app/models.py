from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class Vendor(models.Model):
    name = models.CharField(max_length=50)
    website = models.CharField(max_length=255)
    logo_url = models.URLField()


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')


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
    category = models.OneToOneField("Category", on_delete=models.CASCADE, related_name='filters')


class ProductImage(models.Model):
    src = models.URLField()
    product_details = models.ForeignKey('ProductVendorDetails', null=True, blank=True, on_delete=models.CASCADE,
                                        related_name='images')


class ProductVendorDetails(models.Model):
    class InventoryState(models.TextChoices):
        IN_STOCK = 'IS', _('In stock')
        OUT_OF_STOCK = 'OOS', _('Out of stock')
        IN_TRANSIT = 'IT', _('In transit')
        ON_COMMAND = 'OC', _('On command')

    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='details')
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    url = models.URLField()
    unit_price = models.FloatField()
    discount_available = models.BooleanField(default=False)
    warranty = models.CharField(max_length=50)
    inventory_state = models.CharField(
        max_length=5,
        choices=InventoryState.choices,
        default=InventoryState.IN_STOCK,
    )


class StartUrl(models.Model):
    url = models.URLField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='start_urls')
    item = models.ForeignKey("ScrapyItem", on_delete=models.CASCADE)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name='start_urls')


class ScrapyItem(models.Model):
    name = models.CharField(max_length=50)
    age = models.URLField()
