import json
import re
import factory

from app.model_factories import CategoryFactory, ProductFactory
from mimesis_factory import MimesisField
from .entity_managers import CategoryManager
from pathlib import Path

from .items import ProductItem

config_path = Path(__file__).resolve().parent.parent / "conf.json"


def make_extractor(category, config_file_location=config_path):
    class ComputerInfoExtractor:
        def __init__(self, computer_regexes):
            self._computer_regexes = computer_regexes

        def extract(self, product_description):
            info = {}
            for field in self._computer_regexes:
                field_info = self.extract_field_info(field, product_description)
                if field_info:
                    info[field] = field_info
            return info

        def extract_field_info(self, field, product_description):
            for pattern, product_format in zip(*self._computer_regexes[field]):
                cp = re.compile(pattern, re.IGNORECASE)
                curr_match = cp.search(product_description)
                if curr_match:
                    return product_format.format(*(curr_match.groups()))

    product_regexes = get_config(config_file_location)

    if CategoryManager.is_descendent_of(category, parent_name="Computers", include_self=True):
        computer_regexes = product_regexes["Computers"]
        return ComputerInfoExtractor(computer_regexes)

    raise NotImplementedError


def get_config(config_file_location):
    with open(config_file_location, 'r') as f:
        product_re = json.load(f)
    return product_re


def make_comparator(category):
    class ComputerComparator:
        def compare(self, product1, product2):
            return product1["category"] == product2["category"] and product1["name"] == product2["name"]

    if CategoryManager.is_descendent_of(category, parent_name="Computers", include_self=True):
        return ComputerComparator()
    raise NotImplementedError


def make_info_merger(category):
    class ComputerInfoMerger:
        @staticmethod
        def merge(old_item, new_item):
            merged_item = old_item.copy()
            if not merged_item.get("name") and new_item.get('name'):
                merged_item["name"] = new_item['name']

            if not merged_item.get('reference') and new_item.get('reference'):
                merged_item['reference'] = new_item['reference']

            if not merged_item.get('image_url') and new_item.get('image_url'):
                merged_item['image_url'] = new_item['image_url']
            return merged_item

    if CategoryManager.is_descendent_of(category, parent_name="Computers", include_self=True):
        return ComputerInfoMerger()
    raise NotImplementedError


class ProductItemFactory(factory.Factory):
    class Meta:
        model = ProductItem
        exclude = ('vendor_name', 'num_of_years')

    name = "Sample Product"
    category = factory.SubFactory(CategoryFactory)
    image_url = factory.LazyAttribute(lambda product_item: f'{product_item.name}.image.com')
    reference = factory.LazyAttributeSequence(lambda product_item, count: f'{product_item.name}-{count}')
    price = MimesisField("float_number", start=0, precision=2)
    characteristics = factory.Dict(dict(color=MimesisField("color")))
    vendor_name = MimesisField('company')
    url = factory.LazyAttribute(lambda product_item: f'{product_item.vendor_name}.com/{product_item.reference}')
    num_of_years = MimesisField("choice", items=range(5))
    warranty = factory.LazyAttribute(lambda pvd: f'{pvd.num_of_years} Year(s)')


