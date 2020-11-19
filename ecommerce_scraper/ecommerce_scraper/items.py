# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GeneralItem(scrapy.Item):
    name = scrapy.Field()
    reference = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    # state = scrapy.Field()
    # discount = scrapy.Field()
    warranty = scrapy.Field()
    image = scrapy.Field()


class LaptopItem(GeneralItem):
    os = scrapy.Field()
    reference = scrapy.Field()
    cpu = scrapy.Field()
    cpu_frequency = scrapy.Field()
    cpu_gen = scrapy.Field()
    cpu_cache = scrapy.Field()
    ram = scrapy.Field()
    ram_type = scrapy.Field()
    # screen_type = scrapy.Field()
    screen_size = scrapy.Field()
    screen_resolution = scrapy.Field()
    screen_frequency = scrapy.Field()
    # touch_screen = scrapy.Field()
    hard_disk = scrapy.Field()
    gpu = scrapy.Field()
    # connections = scrapy.Field()
    # bluetooth = scrapy.Field()
    color = scrapy.Field()


