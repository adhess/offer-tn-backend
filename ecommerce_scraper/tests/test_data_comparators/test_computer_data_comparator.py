import pytest
from ecommerce_scraper.ecommerce_scraper.factories import make_comparator


@pytest.fixture
def computer_info_comparator(category_factory):
    return make_comparator(category=category_factory(name="Computers"))


@pytest.fixture
def gaming_laptops(category_factory):
    return category_factory(name="gaming_laptops")


@pytest.fixture
def gaming_laptop1(gaming_laptops, product_item_factory):
    return product_item_factory(name="ASUS ROG", category=gaming_laptops)


@pytest.fixture
def gaming_laptop2(gaming_laptops, product_item_factory):
    return product_item_factory(name="ASUS ROG", category=gaming_laptops)


@pytest.fixture
def gaming_laptop3(gaming_laptops, product_item_factory):
    return product_item_factory(name="MSI GP62", category=gaming_laptops)


@pytest.fixture
def macbook(category_factory, product_item_factory):
    return product_item_factory(name="Macbook Air", category=category_factory(name="macbooks"))


def test_returns_true_for_products_with_same_name_and_category(db, computer_info_comparator, gaming_laptop1, gaming_laptop2):
    assert computer_info_comparator.compare(gaming_laptop1, gaming_laptop2)


def test_returns_false_for_products_with_different_names(db, computer_info_comparator, gaming_laptop1, gaming_laptop3):
    assert computer_info_comparator.compare(gaming_laptop1, gaming_laptop3) is False


def test_returns_false_for_products_with_different_categories(db, computer_info_comparator, gaming_laptop1, macbook):
    assert computer_info_comparator.compare(gaming_laptop1, macbook) is False



