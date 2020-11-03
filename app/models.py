from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Vendor(models.Model):
    name = models.CharField(max_length=50)
    website = models.CharField(max_length=255)


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='children')


class Product(models.Model):
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=255)
    image = models.URLField()
    characteristics = models.JSONField()
    popularity = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='products')


class Filter(models.Model):
    characteristics = models.JSONField()
    # characteristics = {cpu: "checkbox"}
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='filters')


class ProductVendorDetails(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_from_all_vendors")
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name="products")
    url = models.URLField()
    unit_price = models.FloatField()
    discount_available = models.BooleanField(default=False)
    warranty = models.CharField(max_length=50)
    inventory_state = models.CharField(max_length=50)


class StartUrl(models.Model):
    url = models.URLField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='start_urls')
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name='start_urls')

