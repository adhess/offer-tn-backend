import pytest
from scrapy.exceptions import DropItem
from app.models import Product, ProductVendorDetails
from ecommerce_scraper.ecommerce_scraper.entity_managers import (
    CategoryManager, ProductVendorDetailsManager, ProductManager)
from ecommerce_scraper.ecommerce_scraper.items import ProductItem


@pytest.fixture
def computers(category_factory, electronics):
    return category_factory(name="Computers", parent=electronics, is_active=True)


@pytest.fixture
def regular_laptops(category_factory, computers):
    return category_factory(name="Regular Laptops", parent=computers, is_active=True)


@pytest.fixture
def desktop(computers, category_factory):
    return category_factory(name="Desktop", parent=computers, is_active=True)


@pytest.fixture
def electronics(category_factory):
    return category_factory(name="Electronics", is_active=True)


@pytest.fixture
def clothes(category_factory):
    return category_factory(name="Clothes", is_active=True)


@pytest.fixture
def sample_product(product_factory):
    return product_factory()


@pytest.fixture
def sample_vendor(vendor_factory):
    return vendor_factory()


@pytest.fixture
def product_item(product_item_factory, sample_product):
    return product_item_factory(product=sample_product)

@pytest.mark.django_db
class TestCategoryManager:
    def test_is_descendent_of(self, regular_laptops, computers):
        assert CategoryManager.is_descendent_of(regular_laptops, "Computers")
        assert CategoryManager.is_descendent_of(regular_laptops, "Electronics")
        assert CategoryManager.is_descendent_of(computers, regular_laptops) is False

    def test_include_self_flag(self, regular_laptops):
        assert CategoryManager.is_descendent_of(regular_laptops, "Regular Laptops") is False
        assert CategoryManager.is_descendent_of(regular_laptops, "Regular Laptops", include_self=True)


@pytest.mark.django_db
class TestProductManager:
    def test_create_new_product_from_item(self, product_item):
        new_product = ProductManager.create_new_product(product_item)

        assert Product.objects.get(name=product_item["name"], category=product_item["category"]) == new_product

    def test_create_new_item_raises_drop_item_for_missing_item_fields(self):
        with pytest.raises(DropItem):
            item = ProductItem()
            ProductManager.create_new_product(item)

    def test_create_new_item_raises_drop_item_for_violating_not_null_constraint(self, product_item_factory):
        with pytest.raises(DropItem):
            product_item = product_item_factory(name=None)
            ProductManager.create_new_product(product_item)

    def test_update_with_item_is_in_place(self, sample_product, product_item):
        old_id = sample_product.id
        ProductManager.update_with_item(sample_product, product_item)
        assert sample_product.id == old_id

    def test_update_with_item_updates_product_correctly(self, sample_product, product_item):
        ProductManager.update_with_item(sample_product, product_item)

        assert sample_product.name == product_item["name"]
        assert sample_product.reference == product_item["reference"]
        assert sample_product.image_url == product_item["image_url"]
        assert sample_product.characteristics == product_item["characteristics"]

    def test_update_with_item_saves_updated_product_to_db(self, sample_product, product_item):
        ProductManager.update_with_item(sample_product, product_item)

        product_in_db = Product.objects.get(pk=sample_product.pk)
        assert product_in_db == sample_product

    def test_to_dict_returns_dict(self, sample_product):
        sample_product_dict = ProductManager.to_dict(sample_product)
        assert isinstance(sample_product_dict, dict)

    def test_get_similar_products(self, product_item_factory, regular_laptops, clothes, desktop):
        laptop_item = product_item_factory(name="laptop0", category=regular_laptops)
        laptop1 = ProductManager.create_new_product(product_item_factory(name="laptop1", category=regular_laptops))
        laptop2 = ProductManager.create_new_product(product_item_factory(name="laptop2", category=regular_laptops))
        ProductManager.create_new_product(product_item_factory(name="desktop", category=desktop))
        ProductManager.create_new_product(product_item_factory(name="clothes", category=clothes))

        assert list(ProductManager.get_similar_products(laptop_item)) == [laptop1, laptop2]


@pytest.mark.django_db
class TestProductVendorDetailsManager:
    @pytest.fixture
    def sample_product_vendor_details(self, product_vendor_details_factory):
        return product_vendor_details_factory()

    def test_creates_instance_in_db(self, product_item, sample_vendor, sample_product):
        product_vendor_details = ProductVendorDetailsManager.create_product_vendor_details(
            product_item,
            vendor=sample_vendor)

        saved_product_vendor_details = ProductVendorDetails.objects.get(
            product=product_item["product"],
            vendor=sample_vendor,
            warranty=product_item["warranty"],
            link_in_vendor_website=product_item["url"],
            registered_prices=[product_item["price"]])
        assert product_vendor_details == saved_product_vendor_details

    def test_create_new_item_raises_drop_item_for_missing_item_fields(self, sample_vendor):
        with pytest.raises(DropItem):
            product_item = ProductItem()
            ProductVendorDetailsManager.create_product_vendor_details(product_item, vendor=sample_vendor)

    def test_create_new_item_raises_drop_item_for_violating_not_null_constraint(self, product_item):
        with pytest.raises(DropItem):
            ProductVendorDetailsManager.create_product_vendor_details(product_item, vendor=sample_vendor)

    def test_get_product_vendor_details(self, sample_product_vendor_details):
        saved_product_vendor_details = ProductVendorDetailsManager.get_product_vendor_details(
            product=sample_product_vendor_details.product,
            vendor=sample_product_vendor_details.vendor)
        assert sample_product_vendor_details == saved_product_vendor_details

    def test_update_with_item_is_inplace(self, sample_product_vendor_details, sample_product, product_item):
        old_id = sample_product_vendor_details.id

        ProductVendorDetailsManager.update_with_item(sample_product_vendor_details, product_item)

        assert sample_product_vendor_details.id == old_id

    def test_update_with_item_updates_instance_correctly(self, sample_product_vendor_details, sample_product, product_item):
        old_registered_prices = sample_product_vendor_details.registered_prices.copy()

        ProductVendorDetailsManager.update_with_item(
            sample_product_vendor_details,
            product_item)

        assert sample_product_vendor_details.warranty == product_item['warranty']
        assert sample_product_vendor_details.link_in_vendor_website == product_item['url']
        assert sample_product_vendor_details.registered_prices == old_registered_prices + [product_item['price']]

    def test_update_with_item_saves_updated_instance_to_db(self, sample_product_vendor_details, product_item):
        ProductVendorDetailsManager.update_with_item(sample_product_vendor_details, product_item)

        product_vendor_details_in_db = ProductVendorDetails.objects.get(pk=sample_product_vendor_details.pk)
        assert product_vendor_details_in_db == sample_product_vendor_details
