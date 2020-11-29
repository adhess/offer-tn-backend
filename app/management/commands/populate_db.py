import random

from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import *
from .mock_data import categories, images, start_urls
import string
import pyclbr
import sys
from pathlib import Path


sys.path.append(str(Path('app').resolve().parent.joinpath('ecommerce_scraper', 'ecommerce_scraper')))


class Command(BaseCommand):
    help = 'Populates the database with data'

    def add_arguments(self, parser):
        parser.add_argument("-a", "--all", action="store_true", help="populate the entire database")

    def get_leaf_categories(self, arr, data, parent):
        category = Category(name=data['name'], icon=data['icon'], active=data['active'], parent=parent)
        category.save()
        if 'children' in data:
            for d in data['children']:
                self.get_leaf_categories(arr, d, category)
        else:
            arr.append(category)

    @staticmethod
    def get_random_string():
        letters = string.ascii_letters + "0123456789-"
        result_str = ''.join(random.choice(letters) for _ in range(25))
        return result_str

    @staticmethod
    def _populate_vendors():
        vendors = [
            Vendor(name='mytek',
                   website='https://mytek.tn/',
                   logo_url='https://web-assets-mk.s3.amazonaws.com/img/mytek-informatique-logo-1482243620.jpg',
                   css_selectors=dict(product_selector='#center_column .product-name',
                                      pagination_selector='#pagination_next_bottom a',
                                      specs_selector='#idTab2 td',
                                      image_selector='#bigpic::attr(src)',
                                      ref_selector='.editable::text',
                                      name_selector='h1::text',
                                      price_selector='#our_price_display::text',
                                      )),
            Vendor(name='tunisianet', website='https://www.tunisianet.com.tn/',
                   logo_url='https://www.tunisianet.com.tn/img/tunisianet-logo-1573421421.jpg'),
            Vendor(name='wiki',
                   website='https://www.wiki.tn/',
                   logo_url='https://www.wiki.tn/img/logo.jpg',
                   css_selectors=dict(product_selector='#product_list .product-name',
                                      pagination_selector='#pagination_next_bottom a',
                                      specs_selector='td',
                                      image_selector='#bigpic::attr(src)',
                                      ref_selector='.editable::text',
                                      name_selector='h1::text',
                                      price_selector='#our_price_display::text',
                                      )),
            Vendor(name='scoop', website='https://www.scoop.com.tn/',
                   logo_url='https://www.scoop.com.tn/img/sp-g3shop-logo-1591977520.jpg'),
            Vendor(name='sbsinformatique', website='https://www.sbsinformatique.com/',
                   logo_url='https://www.sbsinformatique.com/img/prestashop-logo-1585766163.jpg'),
        ]
        for v in vendors:
            v.save()
        return vendors

    def _populate_categories(self):
        leaf_categories = []
        for c in categories:
            self.get_leaf_categories(arr=leaf_categories, data=c, parent=None)
        return leaf_categories

    @staticmethod
    def _populate_scrapy_items():
        module_name = 'items'
        module_info = pyclbr.readmodule(module_name)
        return [ScrapyItem.objects.create(name=item.name) for item in module_info.values()]

    @staticmethod
    def _populate_start_urls(leaf_categories, vendors, scrapy_items):
        for vendor in vendors:
            for item in scrapy_items:
                for category in leaf_categories:
                    if vendor.name in start_urls:
                        if item.name in start_urls[vendor.name]:
                            if category.name in start_urls[vendor.name][item.name]:
                                StartUrl.objects.create(
                                    url=start_urls[vendor.name][item.name][category.name],
                                    category=category,
                                    vendor=vendor,
                                    item=ScrapyItem.objects.get(name='LaptopItem')
                                )

    def _populate_product(self, leaf_categories=None, vendors=None):
        for category in leaf_categories:
            for k in range(30, 100):
                product = Product(
                    category=category,
                    characteristics={
                        'Processor': 'i' + str(2 * random.randint(1, 4) + 1) + '-' + str(
                            random.randint(2000, 11986)) + 'H',
                        'Graphic card': 'NVIDIA GeForce ' + (
                            'GTX' if random.randint(0, 1) % 2 == 1 else 'RTX') + ' ' + str(
                            random.randint(1000, 3200)) + ' (4 Go GDDR5)',
                        'Screen': ['17.3"', '15.6"', '14"', '13.3"', '12"'][random.randint(0, 4)] + (
                            '' if random.randint(0, 1) % 2 == 1 else 'Full') + ' HD',
                        'RAM': str(random.randint(2, 128)) + ' Go DDR4',
                        'OS': ['FreeDos', 'Ubuntu', 'Windows'][random.randint(0, 2)],
                        'color': ['black', 'red', 'blue', 'pink'][random.randint(0, 3)]
                    },
                    name='best computer ever ' + self.get_random_string(),
                    image_url=images[category.name][random.randint(0, len(images[category.name]) - 1)],
                    popularity=random.randint(15, 100),
                    ref=self.get_random_string()
                )
                product.save()

                for j in range(random.randint(1, 3)):
                    stat = ["IS", "OOS", "IT", "OC"]
                    registered_prices = []
                    for i in range(0, 15):
                        length = len(registered_prices)
                        price = 0 if length == 0 else registered_prices[length - 1]
                        registered_prices.append(
                            price if length > 0 and random.randint(0, 1) == 0 else random.randint(1000, 7000)
                        )
                    product_details = ProductVendorDetails(
                        discount_available=random.randint(0, 1) % 2 == 1,
                        inventory_state=stat[random.randint(0, 3)],
                        product=product,
                        url='https://www.wiki.tn/pc-portables-gamer/pc-portable-gamer-asus-zenbook-pro-duo-i9-10e-gen-32go-1to-ssd-32231.html',
                        vendor=vendors[random.randint(0, 4)],
                        warranty=['1 ans', '2 ans', '3 ans', '4 ans', '5 ans'][random.randint(0, 4)],
                        registered_prices=registered_prices,
                    )
                    product_details.save()

    @transaction.atomic()
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        for model in [ProductVendorDetails, Product, StartUrl, ScrapyItem, Vendor, Category]:
            model.objects.all().delete()

        self.stdout.write("Creating new data...")

        leaf_categories = self._populate_categories()
        vendors = self._populate_vendors()
        scrapy_items = self._populate_scrapy_items()
        self._populate_start_urls(leaf_categories, vendors, scrapy_items)
        if options["all"]:
            self._populate_product(leaf_categories, vendors)

        self.stdout.write("okay")
