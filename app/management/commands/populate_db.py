import random

from django.core.management.base import BaseCommand
from app.models import *

from .mock_data import mock_data
import string


def get_random_string():
    letters = string.ascii_letters + "0123456789-"
    result_str = ''.join(random.choice(letters) for i in range(25))
    return result_str


def _populate(self):
    vendors = [
        Vendor(name='myteck', website='https://mytek.tn/',
               logo_url='https://web-assets-mk.s3.amazonaws.com/img/mytek-informatique-logo-1482243620.jpg'),
        Vendor(name='tunisianet', website='https://www.tunisianet.com.tn/',
               logo_url='https://www.tunisianet.com.tn/img/tunisianet-logo-1573421421.jpg'),
        Vendor(name='wiki', website='https://www.wiki.tn/', logo_url='https://www.wiki.tn/img/logo.jpg'),
        Vendor(name='scoop', website='https://www.scoop.com.tn/',
               logo_url='https://www.scoop.com.tn/img/sp-g3shop-logo-1591977520.jpg'),
        Vendor(name='sbsinformatique', website='https://www.sbsinformatique.com/',
               logo_url='https://www.sbsinformatique.com/img/prestashop-logo-1585766163.jpg'),
    ]
    images = [
        'https://www.wiki.tn/54636-home_default_mobi/pc-portable-hp-pavilion-gaming-15-ec0006nk-amd-8go-1to128go-gtx-3go.jpg',
        'https://www.wiki.tn/52149-home_default_mobi/pc-portable-gamer-lenovo-l340-i5-9e-gen-8go-2to-noir-.jpg',
        'https://www.wiki.tn/52155-home_default_mobi/pc-portable-gamer-lenovo-l340-i5-9e-gen-16go-2to-noir.jpg',
        'https://www.wiki.tn/53841-home_default_mobi/pc-portable-asus-f571lh-i5-10e-8go-512-go-ssd-4g-win10-noir.jpg',
        'https://www.wiki.tn/52252-home_default_mobi/pc-portable-gamer-lenovo-l340-i7-9e-gen-8go-2to-gtx1050-noir.jpg',
        'https://www.wiki.tn/54494-home_default_mobi/pc-portable-acer-nitro-5-an515-54-i5-9e-gen-16go-1to128go-ssd.jpg',
        'https://www.wiki.tn/55286-home_default_mobi/pc-portable-gamer-msi-gf63-thin-10scxr-i5-10e-gen-32go-512go-gtx1650.jpg',
        'https://www.wiki.tn/43304-home_default_mobi/pc-portable-lenovo-legion-y540-i5-9e-gen-8go-1to128go-ssd.jpg',
        'https://www.wiki.tn/53275-home_default_mobi/pc-portable-gamer-asus-tuf-506ii-bq243t-amd-8go-512go-ssd-4go-win10.jpg',
        'https://www.wiki.tn/52462-home_default_mobi/pc-portable-acer-predator-ph317-52-75db-i7-8e-gen-8-go-128-ssd-1to-win10.jpg',
        'https://www.wiki.tn/52605-home_default_mobi/pc-portable-gamer-lenovo-l340-i7-9e-gen-16go-2to256ssd-1650gtx.jpg',
        'https://www.wiki.tn/53619-home_default_mobi/pc-portable-asus-tuf-a15-amd-ryzen-r7-8go-512go-gtx1660ti-gris.jpg',
        'https://www.wiki.tn/55797-home_default_mobi/pc-portable-gamer-lenovo-legion5-ryzen-7-16go-1to-128go-4-go.jpg',
        'https://www.wiki.tn/55740-home_default_mobi/pc-portable-gamer-asus-rog-strix-g512li-i7-10e-gen-8go-512-go-win10.jpg',
        'https://www.wiki.tn/54083-home_default_mobi/pc-portable-gamer-asus-rog-strix-g15-i7-10e-gen-8go-512-go-ssd.jpg',
    ]
    for v in vendors:
        v.save()

    for c in mock_data:
        category = Category(name=c['name'])
        category.save()
        for sc in c['children']:
            sub_category = Category(name=sc['name'], parent=category)
            sub_category.save()
            for ssc in sc['children']:
                sub_sub_category = Category(name=ssc['name'], parent=sub_category)
                sub_sub_category.save()
                for i in range(random.randint(15, 100)):
                    image = ProductImage(src=images[random.randint(1, len(images) - 1)])
                    image.save()
                    product = Product(
                        category=sub_sub_category,
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
                        name='best computer ever xg78ti',
                        one_image=image,
                        popularity=random.randint(15, 100),
                        ref=get_random_string()
                    )
                    product.save()
                    for j in range(random.randint(1, 3)):
                        stat = [
                            ProductVendorDetails.InventoryState.IN_STOCK,
                            ProductVendorDetails.InventoryState.IN_TRANSIT,
                            ProductVendorDetails.InventoryState.ON_COMMAND,
                            ProductVendorDetails.InventoryState.OUT_OF_STOCK,
                        ]
                        product_details = ProductVendorDetails(
                            discount_available=random.randint(0, 1) % 2 == 1,
                            inventory_state=stat[random.randint(0, 3)],
                            product=product,
                            unit_price=random.randint(1000, 7000),
                            url='https://www.wiki.tn/pc-portables-gamer/pc-portable-gamer-asus-zenbook-pro-duo-i9-10e-gen-32go-1to-ssd-32231.html',
                            vendor=vendors[random.randint(0, 4)],
                            warranty=['1 ans', '2 ans', '3 ans', '4 ans', '5 ans'][random.randint(0, 4)]
                        )
                        product_details.save()
                        for i in range(random.randint(0, 10)):
                            p = ProductImage(src=[images[random.randint(0, len(images) - 1)]], product_details=product_details)
                            p.save()


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        _populate(self)
        self.stdout.write("okay")
