from django.contrib import admin

# Register your models here.
from app.models import (
    Category, Vendor, StartUrl, ScrapyItem, Product, ProductVendorDetails
)

# Register your models here. admin.site.register(Flight)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'active', 'parent')


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')


@admin.register(StartUrl)
class StartUrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'category', 'item', 'vendor')


@admin.register(ScrapyItem)
class ScrapyItemAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'ref', 'category', 'characteristics', 'popularity')


@admin.register(ProductVendorDetails)
class ProductVendorDetailsAdmin(admin.ModelAdmin):
    list_display = ('product', 'vendor', 'url', 'discount_available', 'warranty', 'inventory_state', 'registered_prices')




