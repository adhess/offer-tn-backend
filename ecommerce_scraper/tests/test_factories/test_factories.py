import re

from app.models import Category, Product
from ecommerce_scraper.ecommerce_scraper.factories import make_extractor, make_comparator, make_info_merger
import pytest


@pytest.fixture
def computers(category_factory):
    return category_factory(name="Computers", is_active=True)


@pytest.fixture
def regular_laptops(computers, category_factory):
    return category_factory(name="Regular Laptop", parent=computers, is_active=True)


@pytest.fixture
def glasses(category_factory):
    return category_factory(name="Glasses", is_active=True)


@pytest.mark.parametrize(("factory", "expected_class"), [(make_extractor, 'ComputerInfoExtractor'),
                                                         (make_comparator, "ComputerComparator"),
                                                         (make_info_merger, "ComputerInfoMerger")])
def test_factory_returns_correct_class_for_computers(factory, expected_class, db, computers, regular_laptops):
    output = factory(category=computers)
    assert output.__class__.__name__ == expected_class
    output = factory(category=regular_laptops)
    assert output.__class__.__name__ == expected_class


@pytest.mark.parametrize("factory", [make_extractor, make_comparator, make_info_merger])
def test_factory_raises_error_for_non_implemented_categories(factory, db, glasses):
    with pytest.raises(NotImplementedError):
        factory(glasses)


@pytest.mark.django_db
class TestProductItemFactory:
    @pytest.fixture
    def product_item(self, product_item_factory):
        return product_item_factory(__sequence=1)

    def test_default_name_value(self, product_item):
        assert product_item['name'] == "Sample Product"

    def test_default_category_is_valid_category(self, product_item):
        assert isinstance(product_item["category"], Category)

    def test_default_category_is_saved_to_db(self, product_item_factory):
        assert Category.objects.filter(name="category-1").exists() is False
        product_item = product_item_factory(category____sequence=1)
        assert Category.objects.get(name="category-1")

    def test_default_product_is_a_missing_field(self, product_item):
        with pytest.raises(KeyError):
            product = product_item["product"]

    def test_default_price_is_float(self, product_item):
        assert type(product_item["price"]) == float

    def test_default_format_of_image_url(self, product_item):
        assert product_item["image_url"] == product_item["name"] + ".image.com"

    def test_default_format_of_link_in_vendor_website(self, product_item):
        assert product_item["url"].endswith(f".com/{product_item['reference']}")

    def test_default_reference_format(self, product_item):
        assert product_item["reference"] == product_item["name"] + "-1"

    def test_default_characteristics_is_dict_with_color_field(self, product_item):
        characteristics = product_item["characteristics"]
        assert isinstance(characteristics, dict)
        assert isinstance(characteristics["color"], str)

    def test_default_reference_increments(self, product_item_factory):
        product_item_factory.reset_sequence()
        first_product_item = product_item_factory()
        second_product_item = product_item_factory()

        assert first_product_item["reference"][-1] == '0'
        assert second_product_item["reference"][-1] == '1'

    def test_default_warranty_format(self, product_item):
        warranty = product_item['warranty']
        assert re.fullmatch(r'\d Year\(s\)', warranty)
