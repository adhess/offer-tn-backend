# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
from app.models import ProductVendorDetails, Product, Vendor
from django.db import transaction
from datetime import datetime

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
                specs[field] = item[field]

    @staticmethod
    def update_product_vendor_details(product_vendor_details, item):
        #Todo update remaoning fields

        product_vendor_details.url = item['url']
        product_vendor_details.warranty = item['warranty']
        product_vendor_details.registered_prices.append(item['price'])


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        with transaction.atomic():
            existing_product = Product.objects.get(
                ref=adapter['reference'],
                characteristics={'ram': adapter['ram'], 'ssd': adapter['ssd'], 'hard_disk': adapter['hard_disk']}
            )

            if existing_product:
                self.update_product(existing_product, adapter)
            else:
                product = Product(
                    name=adapter['name'],
                    ref=adapter['ref'],
                    category=adapter['category'],
                    image_url=adapter['image'],
                    characteristics={
                        'os': adapter['os'],
                        'reference': adapter['reference'],
                        'cpu': adapter['cpu'],
                        'cpu_frequency': adapter['cpu_frequency'],
                        'cpu_gen': adapter['cpu_gen'],
                        'cpu_cache': adapter['cpu_cache'],
                        'ram': adapter['ram'],
                        'ram_type': adapter['ram_type'],
                        'screen_size': adapter['screen_size'],
                        'screen_resolution': adapter['screen_resolution'],
                        'screen_frequency': adapter['screen_frequency'],
                        'hard_disk': adapter['hard_disk'],
                        'ssd': adapter['ssd'],
                        'gpu': adapter['gpu'],
                        'color': adapter['color'],
                    }
                )
                product.save()

            vendor = Vendor.objects.get(name=spider.name.capitalize())
            existing_details = product.details.filter(vendor=vendor)  #Todo find out if this is optimal or not
            if existing_details:
                self.update_product_vendor_details(existing_details, adapter)

            else:
                product_vendor_details = ProductVendorDetails(
                    product=product,
                    vendor=vendor,
                    url=adapter['url'],
                    warranty=adapter['warranty'],
                    registered_prices=[adapter['price']],
                )
                product_vendor_details.save()


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open(f'{spider.name}_items.jl', 'w')


    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item