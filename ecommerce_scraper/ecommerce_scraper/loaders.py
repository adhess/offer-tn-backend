from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, Join, Identity, Compose, TakeFirst
from w3lib.html import remove_tags, unquote_markup
from .items import ProductItem


class PriceFormatter:
    def __init__(self):
        self.price_units = ["TND", "DT"]
        self._prices = []

    def __call__(self, price_strings, loader_context):
        self._prices = []
        self.price_units = loader_context.get("price_units", self.price_units)
        for price_string in price_strings:
            self._prices.append(self._format_price(price_string))

        return self._prices

    def _format_price(self, price_string):
        price_string = price_string.replace(' ', '').replace(',', '.')
        price_string = self._strip_price_units(price_string)
        return float(price_string)

    def _strip_price_units(self, price_string):
        for unit in self.price_units:
            for u in (unit, unit.lower(), unit.capitalize()):
                price_string = price_string.rstrip(u)
        return price_string


class ProductLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

    price_in = PriceFormatter()

    description_in = MapCompose(remove_tags, unquote_markup)
    description_out = Join(', ')


