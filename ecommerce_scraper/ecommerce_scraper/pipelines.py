# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from django.db import transaction
from scrapy.exceptions import DropItem
from ecommerce_scraper.ecommerce_scraper.factories import make_info_merger, make_extractor, make_comparator
from ecommerce_scraper.ecommerce_scraper.entity_managers import ProductVendorDetailsManager, ProductManager


class InfoExtractionPipeline:

    def process_item(self, item, spider):
        extractor = make_extractor(item['category'])
        info = extractor.extract(item['description'])
        self.fill_item_with_extracted_info(item, info)
        return item

    def fill_item_with_extracted_info(self, item, info):
        if info.get("warranty"):
            item["warranty"] = info.pop("warranty")
        item["characteristics"] = info


class ProductPipeline:
    def process_item(self, item, spider):
        product = self._process_item_to_product(item)
        item['product'] = product
        return item

    @transaction.atomic()
    def _process_item_to_product(self, item):
        product = self._get_product_corresponding_to_item(item)
        if not product:
            return ProductManager.create_new_product(item)
        self._merge_existing_product_with_item(product, item)
        return product

    def _get_product_corresponding_to_item(self, item):
        candidate_products = ProductManager.get_similar_products(item)
        product_comparator = make_comparator(["category"])
        for candidate_product in candidate_products:
            if product_comparator.compare(ProductManager.to_dict(candidate_product), item):
                return candidate_product

    def _merge_existing_product_with_item(self, product, item):
        merger = make_info_merger(item['category'])
        item = merger.merge(ProductManager.to_dict(product), item)
        ProductManager.update_with_item(product, item)


class ProductVendorDetailsPipeline:
    def __init__(self, vendor):
        self._vendor = vendor

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.spider.vendor)

    def process_item(self, item, spider):
        if not item['product']:
            raise DropItem('No corresponding product in database')

        with transaction.atomic():
            self._process_item_to_product_vendor_details(item)

        return item

    def _process_item_to_product_vendor_details(self, item):
        product = item['product']
        product_vendor_details = (ProductVendorDetailsManager.
                                  get_product_vendor_details(product, self._vendor))
        if not product_vendor_details:
            return ProductVendorDetailsManager.create_product_vendor_details(item, self._vendor)

        return ProductVendorDetailsManager.update_with_item(product_vendor_details, item)

