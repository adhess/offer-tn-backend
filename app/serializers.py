from rest_framework import serializers
from app.models import Category, Vendor, Product, ProductVendorDetails, Filter
from rest_framework_recursive.fields import RecursiveField


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'children', 'icon', 'is_active']


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'website']


class ProductVendorDetailsSerializers(serializers.HyperlinkedModelSerializer):
    vendor = VendorSerializer(many=False, read_only=True)
    product = serializers.HyperlinkedRelatedField(view_name='products-detail', read_only=True)

    class Meta:
        model = ProductVendorDetails
        fields = ['id', 'url', 'product', 'vendor', 'link_in_vendor_website', 'registered_prices',
                  'is_discount_available', 'warranty', 'inventory_state']


class ProductSerializers(serializers.HyperlinkedModelSerializer):
    details = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='products-detail')
    category = serializers.HyperlinkedRelatedField(view_name='categories-detail', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'reference', 'category', 'details', 'characteristics', 'popularity', 'image_url', 'minimum_price']


class FilterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = ['fields']
