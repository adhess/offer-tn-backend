import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ecommerce_scraper.spiders.mytek import MytekSpider

process = CrawlerProcess(get_project_settings())

with open('conf.json', 'r') as f:
    regexes = json.load(f)

# TODO get these parameters from the database
# TODO find solution to duplicate products from different links having the wrong category
mytek_urls = [
    'https://www.mytek.tn/13-pc-portable#/gamer-oui',
    'https://www.mytek.tn/13-pc-portable',
    'https://www.mytek.tn/379-mac',
    'https://www.mytek.tn/13-pc-portable#/type-ultrabook',
]

wiki_urls = [
    'https://www.wiki.tn/c/pc-portable-120.html',
    'https://www.wiki.tn/c/pc-portable-gamer-85.html',
    'https://www.wiki.tn/c/macbook-568.html',
    'https://www.wiki.tn/c/transformer-121.html',
]


# jumia_urls = ['https://jumia.com.tn/pc-gamer-2139/',
#               'https://jumia.com.tn/pc-portables/',]


categories = ['Gamer', 'Regularlaptop', 'Mac', 'Ultrabook']


items = ['Laptop'] * 4


process.crawl(MytekSpider,
              name='mytek',
              urls=mytek_urls,
              categories=categories,
              items=items,
              product_selector='#center_column .product-name',
              pagination_selector='#pagination_next_bottom a',
              specs_selector='#idTab2 td',
              image_selector='#bigpic::attr(src)',
              ref_selector='.editable::text',
              name_selector='h1::text',
              price_selector='#our_price_display::text',
              product_re=regexes,
              )

process.crawl(MytekSpider,
              name='wiki',
              urls=wiki_urls,
              categories=categories,
              items=items,
              product_selector='#product_list .product-name',
              pagination_selector='#pagination_next_bottom a',
              specs_selector='td',
              image_selector='#bigpic::attr(src)',
              ref_selector='.editable::text',
              name_selector='h1::text',
              price_selector='#our_price_display::text',
              product_re=regexes,
              )


# TODO make the scraper work with Jumia

# process.crawl(MytekSpider,
#               name='jumia',
#               urls=jumia_urls,
#               categories=categories,
#               scrapy_items=scrapy_items,
#               product_selector='.info .name',
#               pagination_selector='.pg:nth-last-child(2)',
#               specs_selector='..-pam li',
#               image_selector='#imgs .-fh.-fw::attr(data-src)',
#               ref_selector=None,
#               name_selector='.-pts.-pbxs::text',
#               price_selector='.-fs24::text',
#               product_re=regexes,
#               )



process.start()  # the script will block here until the crawling is finished
