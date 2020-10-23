from django.core.management.base import BaseCommand
from app.models import Category
from app.models import Product
from app.models import Filter
from app.models import Details


def _populate(self):
    category_1 = Category(name="Computers")
    product = Product(ref="xf7-dt65o-p2ie6-nf65", popularity=50,
                      characteristics={'data': [{'name': 'Processor', 'value': '...'}]},
                      category=category_1)
    category_1.save()
    product.save()

    self.stdout.write('is it okay ?')


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        _populate(self)
        self.stdout.write("okay")
