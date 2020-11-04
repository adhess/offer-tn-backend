from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here. admin.site.register(Flight)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(StartUrl)
admin.site.register(Product)
admin.site.register(ProductVendorDetails)
admin.site.register(ProductImage)


