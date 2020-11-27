import random
from datetime import datetime, timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import *


from .mock_data import categories, images
import string


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
            Vendor(name='mytek', website='https://mytek.tn/',
                   logo_url='https://web-assets-mk.s3.amazonaws.com/img/mytek-informatique-logo-1482243620.jpg'),
            Vendor(name='tunisianet', website='https://www.tunisianet.com.tn/',
                   logo_url='https://www.tunisianet.com.tn/img/tunisianet-logo-1573421421.jpg'),
            Vendor(name='wiki', website='https://www.wiki.tn/', logo_url='https://www.wiki.tn/img/logo.jpg'),
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
                    date = datetime(2019, 3, 5)
                    for i in range(0, 15):
                        length = len(registered_prices)
                        price = 0 if length == 0 else registered_prices[length - 1]
                        registered_prices.append(
                            price if length > 0 and random.randint(0, 1) == 0 else random.randint(1000, 7000)
                        )
                        date += timedelta(7)
                    product_details = ProductVendorDetails(
                        discount_available=random.randint(0, 1) % 2 == 1,
                        inventory_state=stat[random.randint(0, 3)],
                        product=product,
                        unit_price=registered_prices[len(registered_prices) - 1],
                        url='https://www.wiki.tn/pc-portables-gamer/pc-portable-gamer-asus-zenbook-pro-duo-i9-10e-gen-32go-1to-ssd-32231.html',
                        vendor=vendors[random.randint(0, 4)],
                        warranty=['1 ans', '2 ans', '3 ans', '4 ans', '5 ans'][random.randint(0, 4)],
                        registered_prices={'data': registered_prices},
                    )
                    product_details.save()

    @transaction.atomic()
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        call_command('flush')

        self.stdout.write("Creating new data...")

        leaf_categories = self._populate_categories()
        vendors = self._populate_vendors()

        if options["all"]:
            self._populate_product(leaf_categories, vendors)

        self.stdout.write("okay")
