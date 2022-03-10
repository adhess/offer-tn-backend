from django.contrib import admin

# Register your models here.
from app.models import (
    Category, Vendor, StartUrl, Product, ProductVendorDetails
)

# Register your models here. admin.site.register(Flight)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'is_active', 'parent')


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')


@admin.register(StartUrl)
class StartUrlAdmin(admin.ModelAdmin):
    list_display = ('start_url', 'category', 'vendor')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', 'category', 'characteristics', 'popularity')


@admin.register(ProductVendorDetails)
class ProductVendorDetailsAdmin(admin.ModelAdmin):
    list_display = ('product', 'vendor', 'link_in_vendor_website', 'is_discount_available', 'warranty', 'inventory_state', 'registered_prices')




