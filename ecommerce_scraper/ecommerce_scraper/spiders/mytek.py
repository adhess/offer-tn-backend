import re
import ecommerce_scraper.items as items
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class MytekSpider(scrapy.Spider):
    """
    Spider class that crawls websites similar to mytek.com
    """

    def start_requests(self):
        for u, cat, item in zip(self.urls, self.categories, self.items):
            yield scrapy.Request(u, callback=self.parse,
                                 cb_kwargs=dict(category=cat, item=item),
                                 errback=self.errback_httpbin,
                                 dont_filter=False,
                                 )

    def parse(self, response, category=None, item=None, **kwargs):
        product_links = response.css(self.product_selector)
        yield from response.follow_all(product_links,
                                       callback=self.parse_product,
                                       cb_kwargs=dict(category=category, item=item))
        pagination_link = response.css(self.pagination_selector)
        yield from response.follow_all(pagination_link,
                                       callback=self.parse,
                                       cb_kwargs=dict(category=category, item=item))

    # def parse_laptop(self, response, category=None):
    #     laptop = items.LaptopItem()
    #     laptop['name'] = response.css(self.name_selector).get()
    #     laptop['reference'] = response.css(self.ref_selector).get()
    #     laptop["category"] = category
    #     laptop["url"] = response.url
    #     laptop["image"] = response.css(self.image_selector).get()
    #     laptop["price"] = response.css(self.price_selector).get()
    #     specs = ', '.join(response.css(self.specs_selector).re('<[^>]*>([^<]*)<'))
    #     field_re = getattr(self, 'laptop_re')
    #     for field in laptop.fields:
    #         if not laptop.get(field):
    #             patterns, formats = field_re[field].values()
    #             for i, (pattern, product_format) in enumerate(zip(patterns, formats)):
    #                 cp = re.compile(pattern)
    #                 curr_match = cp.search(specs)
    #                 if curr_match:
    #                     laptop[field] = product_format.format(*(curr_match.groups()))
    #                     break
    #     yield laptop

    def parse_product(self, response, category: str, item: str):
        product = getattr(items, f'{item.capitalize()}Item')()
        product['name'] = self.get_field(response, self.name_selector).get()
        product['reference'] = self.get_field(response, self.ref_selector).get()
        product["category"] = category
        product["url"] = response.url
        product["image"] = self.get_field(response, self.image_selector).get() # TODO scrape all product images, not just one
        product["price"] = self.rchop(self.get_field(response, self.price_selector).get(), 'TND')
        specs = ', '.join(self.get_field(response, self.specs_selector).re('<[^>]*>([^<]*)<'))
        field_re = self.product_re[item.lower()]
        for field in product.fields:
            if not product.get(field):
                patterns, formats = field_re[field].values()
                for pattern, product_format in zip(patterns, formats):
                    cp = re.compile(pattern)
                    curr_match = cp.search(specs)
                    if curr_match:
                        product[field] = product_format.format(*(curr_match.groups()))
                        break
        yield product

    @staticmethod
    def rchop(s, *sub):
        return s[:-len(sub)] if s.endswith(sub) else s

    @staticmethod
    def get_field(response, selector=None):
        if selector is None:
            return
        return response.css(selector)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)


