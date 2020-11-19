import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ecommerce_scraper.spiders.mytek import MytekSpider

process = CrawlerProcess(get_project_settings())
with open('conf.json', 'r') as f:
    regexes = json.load(f)

# TODO get these parameters from the database
mytek_urls = ['https://www.mytek.tn/13-pc-portable#/gamer-oui',
              'https://www.mytek.tn/13-pc-portable#/',
              'https://www.mytek.tn/379-mac',
              'https://www.mytek.tn/13-pc-portable#/type-ultrabook',
              ]
mytek_categories = ['Gamer', 'Regular laptop', 'Mac', 'Ultrabook']

parse_methods = ['Laptop'] * 4

process.crawl(MytekSpider,
              name='mytek',
              urls=mytek_urls,
              categories=mytek_categories,
              items = parse_methods,
              product_selector='#center_column .product-name',
              pagination_selector='#pagination_next_bottom a',
              specs_selector='#idTab2 td',
              image_selector='#bigpic::attr(src)',
              ref_selector='.editable::text',
              name_selector='h1::text',
              price_selector='#our_price_display::text',
              product_re=regexes,
              )


process.start()  # the script will block here until the crawling is finished
