from rest_framework import serializers

from app.models import Category, ProductImage, Vendor
from app.models import Product
from app.models import ProductVendorDetails
from app.models import Filter

from rest_framework_recursive.fields import RecursiveField


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'children']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['src']


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class ProductVendorDetailsSerializers(serializers.ModelSerializer):
    vendor = VendorSerializer(many=False, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVendorDetails
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    details = ProductVendorDetailsSerializers(many=True, read_only=True)
    one_image = ProductImageSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        # fields = ['ref', 'characteristics', 'popularity', 'details', 'category']
        fields = '__all__'


class FilterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = '__all__'
