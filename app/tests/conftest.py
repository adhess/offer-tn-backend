import pytest
from app.models import Category, Product, ProductVendorDetails, Vendor
from app.model_factories import CategoryFactory, VendorFactory, ProductFactory, ProductVendorDetailsFactory
from pytest_factoryboy import register

register(CategoryFactory)
register(VendorFactory)
register(ProductFactory)
register(ProductVendorDetailsFactory)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_category(db):
    def make_category(name, parent=None, is_active=False, icon=""):
        return Category.objects.create(name=name, parent=parent, is_active=is_active, icon=icon)
    return make_category


@pytest.fixture
def create_vendor(db):
    def make_vendor(name, website, logo_url):
        return Category.objects.create(name=name, website=website, logo_url=logo_url)
    return make_vendor


@pytest.fixture
def create_product(db):
    def make_product(**kwargs):
        category = Category.objects.get(pk=kwargs.pop('category_id', None))
        return Product.objects.create(**kwargs, category=category)
    return make_product


@pytest.fixture
def create_product_vendor_details(db):
    def make_product_vendor_details(**kwargs):
        return ProductVendorDetails.objects.create(**kwargs)
    return make_product_vendor_details
