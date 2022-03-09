from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


class Vendor(models.Model):
    name = models.CharField(max_length=50)
    website = models.CharField(max_length=255)
    logo_url = models.URLField()
    css_selectors = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.name}'

    __repr__ = __str__


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f'{self.name}'

    __repr__ = __str__


class Product(models.Model):
    name = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    characteristics = models.JSONField(default=dict)
    popularity = models.IntegerField(null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='products')
    image_url = models.TextField()
    minimum_price = models.DecimalField(max_digits=12, decimal_places=3)

    def __str__(self):
        return f'{self.name}'

    __repr__ = __str__


class Filter(models.Model):
    fields = ArrayField(models.CharField(max_length=255))
    category = models.OneToOneField("Category", on_delete=models.CASCADE, related_name='filters')


class ProductVendorDetails(models.Model):
    class InventoryState(models.TextChoices):
        IN_STOCK = 'IS', _('In stock')
        OUT_OF_STOCK = 'OOS', _('Out of stock')
        IN_TRANSIT = 'IT', _('In transit')
        ON_COMMAND = 'OC', _('On command')

    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='details')
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    link_in_vendor_website = models.URLField()
    is_discount_available = models.BooleanField(default=False)
    warranty = models.CharField(max_length=50)
    inventory_state = models.CharField(
        max_length=5,
        choices=InventoryState.choices,
        default=InventoryState.IN_STOCK,
    )
    registered_prices = ArrayField(models.DecimalField(max_digits=12, decimal_places=3))

    def save(self, **kwargs):
        if self.inventory_state in ['IS', 'IT', 'OC']:
            product = self.product
            if self.registered_prices[-1] < product.minimum_price:
                product.minimum_price = self.registered_prices[-1]

        super().save(**kwargs)

    def __str__(self):
        return f'{self.product} from {self.vendor}'

    __repr__ = __str__


class StartUrl(models.Model):
    start_url = models.URLField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='start_urls')
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name='start_urls')

    def __str__(self):
        return f'{self.start_url}'

    __repr__ = __str__


