from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .ecommerce_scraper.spiders.mytek import MySpider
import json


process = CrawlerProcess(get_project_settings())
with open('attributes.json', 'r') as f:
    attributes = json.load(f)

# TODO get these parameters from the database
mytek_urls = []
mytek_categories = []

process.crawl(MySpider,
              name='mytek',
              urls=mytek_urls,
              categories=mytek_categories,
              **attributes['mytek'],
              )


process.start()  # the script will block here until the crawling is finished
