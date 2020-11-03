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
    state = scrapy.Field()
    discount = scrapy.Field()
    warranty = scrapy.Field()
    image = scrapy.Field()


class LaptopItem(GeneralItem):
    os = scrapy.Field()
    processor = scrapy.Field()
    processor_frequency = scrapy.Field()
    core_type = scrapy.Field()
    cache = scrapy.Field()
    ram = scrapy.Field()
    ram_frequency = scrapy.Field()
    screen_type = scrapy.Field()
    screen_size = scrapy.Field()
    screen_resolution = scrapy.Field()
    screen_frequency = scrapy.Field()
    touch_screen = scrapy.Field()
    hard_disk = scrapy.Field()
    graphics_card = scrapy.Field()
    connections = scrapy.Field()
    bluetooth = scrapy.Field()
    color = scrapy.Field()


