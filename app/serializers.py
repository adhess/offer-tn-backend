from rest_framework import serializers

from app.models import Category,  Vendor
from app.models import Product
from app.models import ProductVendorDetails
from app.models import Filter

from rest_framework_recursive.fields import RecursiveField


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'children', 'icon', 'active']


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'website']


class ProductVendorDetailsSerializers(serializers.HyperlinkedModelSerializer):
    vendor = VendorSerializer(many=False, read_only=True)
    product = serializers.HyperlinkedRelatedField(view_name='products-detail', read_only=True)

    class Meta:
        model = ProductVendorDetails
        fields = ['id', 'url', 'product', 'vendor', 'product_url', 'registered_prices',
                  'discount_available', 'warranty', 'inventory_state']


class ProductSerializers(serializers.HyperlinkedModelSerializer):
    details = serializers.HyperlinkedRelatedField(many=True, view_name='productvendordetails-detail', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='products-detail')
    category = serializers.HyperlinkedRelatedField(view_name='categories-detail', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'ref', 'category', 'details', 'characteristics', 'popularity', 'image_url', 'minimum_price']


class FilterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = ['fields']
