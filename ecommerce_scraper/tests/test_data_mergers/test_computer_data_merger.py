import pytest
from ecommerce_scraper.ecommerce_scraper.factories import make_info_merger
from ecommerce_scraper.ecommerce_scraper.items import ProductItem


@pytest.fixture
def computer_info_merger(category_factory):
    return make_info_merger(category=category_factory(name="Computers"))


@pytest.fixture
def gaming_laptop_item(category_factory, product_item_factory):
    return product_item_factory(name="ASUS ROG", category=category_factory(name="gaming_laptops"))


def test_merge_replaces_empty_values_only(db, gaming_laptop_item, computer_info_merger):
    item = ProductItem()
    item["name"] = "ASUS gaming"
    item = computer_info_merger.merge(item, gaming_laptop_item)

    assert item["name"] == "ASUS gaming"
    assert item["reference"] == gaming_laptop_item["reference"]
    assert item["image_url"] == gaming_laptop_item["image_url"]