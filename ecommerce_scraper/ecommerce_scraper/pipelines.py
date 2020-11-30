# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
from app.models import ProductVendorDetails, Product, Vendor
from django.db import transaction

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EcommerceScraperPipeline:

    @staticmethod
    def update_product(product, item):
        # Todo update product, in a more fancy way

        # update product specs
        specs = product.characteristics
        for field in specs:
            if not specs[field]:
                specs[field] = item.get(field)

    @staticmethod
    def update_product_vendor_details(product_vendor_details, item):
        #Todo update remaoning fields

        product_vendor_details.url = item['url']
        product_vendor_details.warranty = item['warranty']
        product_vendor_details.registered_prices.append(item['price'])


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        with transaction.atomic():
            product = Product.objects.filter(
                ref=adapter['reference'],
                # characteristics={'ram': adapter['ram'], 'ssd': adapter['ssd'], 'hard_disk': adapter['hard_disk']}
            )

            if product:
                product = product[0]
                self.update_product(product, adapter)
            else:
                product = Product(
                    name=adapter['name'],
                    ref=adapter['reference'],
                    category=adapter['category'],
                    image_url=adapter['image'],
                    characteristics={
                        'os': adapter.get('os'),
                        'cpu': adapter.get('cpu'),
                        'cpu_frequency': adapter.get('cpu_frequency'),
                        'cpu_gen': adapter.get('cpu_gen'),
                        'cpu_cache': adapter.get('cpu_cache'),
                        'ram': adapter.get('ram'),
                        'ram_type': adapter.get('ram_type'),
                        'screen_size': adapter.get('screen_size'),
                        'screen_resolution': adapter.get('screen_resolution'),
                        'screen_frequency': adapter.get('screen_frequency'),
                        'hard_disk': adapter.get('hard_disk'),
                        'ssd': adapter.get('ssd'),
                        'gpu': adapter.get('gpu'),
                        'color': adapter.get('color'),
                    }
                )
                product.save()

            vendor = Vendor.objects.get(name=spider.name)
            product_vendor_details = product.details.filter(vendor=vendor)  #Todo find out if this is optimal or not
            if product_vendor_details:
                product_vendor_details = product_vendor_details[0]
                self.update_product_vendor_details(product_vendor_details, adapter)

            else:
                product_vendor_details = ProductVendorDetails(
                    product=product,
                    vendor=vendor,
                    url=adapter['url'],
                    warranty=adapter.get('warranty'),
                    registered_prices=[adapter['price']],
                )
                product_vendor_details.save()
        return item


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open(f'{spider.name}_items.jl', 'w')


    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item