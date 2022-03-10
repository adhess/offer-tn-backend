from ecommerce_scraper.ecommerce_scraper.loaders import PriceFormatter, ProductLoader
import pytest


@pytest.fixture
def product_loader(response_stub):
    return ProductLoader(response=response_stub)


@pytest.mark.parametrize("original_price, expected_price",
                         [("118.000 TND", 118),
                          ("118.500 TND", 118.5),
                          ("119.000 DT", 119),
                          ("119.000 DT ", 119),
                          ("128,000 TND", 128)]
                         )
def test_single_price_formatting(original_price, expected_price):
    price_formatter = PriceFormatter()
    formatted_price = price_formatter._format_price(original_price)
    assert formatted_price == expected_price


def test_invalid_price_input_raises_exception():
    price_formatter = PriceFormatter()
    with pytest.raises(ValueError):
        formatted_prices = price_formatter(["invalid_price"], dict())


def test_price_extraction(product_loader):
    product_loader.add_value("price", "2419,000 DT ")
    product = product_loader.load_item()
    assert product["price"] == 2419
