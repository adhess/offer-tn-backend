import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ecommerce_scraper.spiders.mytek import MytekSpider

import os
import sys


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'

import django
django.setup()

from app.models import Vendor, StartUrl



process = CrawlerProcess(get_project_settings())


mytek = Vendor.objects.get(name='mytek')
wiki = Vendor.objects.get(name='wiki')

for vendor in (mytek, wiki):
    urls = StartUrl.objects.filter(vendor=vendor)
    css_selectors = vendor.css_selectors
    process.crawl(MytekSpider,
                  name=vendor.name,
                  urls=(url.start_url for url in urls),
                  categories=(url.category for url in urls),
                  vendor=vendor,
                  **css_selectors,
                  )


#
# process.crawl(MytekSpider,
#               name='mytek',
#               urls=mytek_urls,
#               categories=categories,
#               items=items,
#               product_selector='#center_column .product-name',
#               pagination_selector='#pagination_next_bottom a',
#               specs_selector='#idTab2 td',
#               image_selector='#bigpic::attr(src)',
#               ref_selector='.editable::text',
#               name_selector='h1::text',
#               price_selector='#our_price_display::text',
#               product_re=regexes,
#               )



process.start()  # the script will block here until the crawling is finished
