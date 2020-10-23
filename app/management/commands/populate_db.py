import random

from django.core.management.base import BaseCommand
from app.models import Category
from app.models import Product
from app.models import Filter
from app.models import Details

from .mock_data import mock_data
import string


def get_random_string():
    letters = string.ascii_letters + "0123456789-"
    result_str = ''.join(random.choice(letters) for i in range(25))
    return result_str


def _populate(self):
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
                    product = Product(ref=get_random_string(), popularity=random.randint(15, 100),
                                      characteristics={
                                              'Processor': 'i' + str(2 * random.randint(1, 4) + 1) + '-' + str(
                                                  random.randint(2000, 11986)) + 'H',
                                              'Graphic card': 'NVIDIA GeForce ' + (
                                                  'GTX' if random.randint(0, 1) % 2 == 1 else 'RTX') + ' ' + str(
                                                  random.randint(1000, 3200)) + ' (4 Go GDDR5)',
                                              'Screen': ['17.3"', '15.6"', '14"', '13.3"', '12"'][random.randint(0, 4)]
                                                        + ('' if random.randint(0, 1) % 2 == 1 else 'Full') + ' HD',

                                      },
                                      category=sub_sub_category)
                    product.save()
                    for j in range(random.randint(1, 3)):
                        details = Details(price=random.randint(1000, 7000),
                                          owner=["myteck", "wiki", "tunisianet", "sbsInformatique"][random.randint(0, 3)],
                                          name='MSI GF75 THIN 10SCSR',
                                          characteristics={
                                              'RAM': str(random.randint(2, 128)) + ' Go DDR4',
                                              'OS': ['FreeDos', 'Ubuntu', 'Windows'][random.randint(0, 2)],
                                              'color': ['black', 'red', 'blue', 'pink'][random.randint(0, 3)]
                                          },
                                          product=product)
                        details.save()


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        _populate(self)
        self.stdout.write("okay")
