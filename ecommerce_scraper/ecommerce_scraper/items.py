# Define here the models for your scraped scrapy_items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    reference = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    # state = scrapy.Field()
    # discount = scrapy.Field()
    warranty = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    characteristics = scrapy.Field()
    product = scrapy.Field()
