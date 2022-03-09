from ..loaders import ProductLoader
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class MytekSpider(scrapy.Spider):
    """
    Spider class that crawls websites similar to mytek.com
    """

    def start_requests(self):
        for u, cat in zip(self.urls, self.categories):
            yield scrapy.Request(u, callback=self.parse,
                                 cb_kwargs=dict(category=cat),
                                 errback=self.errback_httpbin,
                                 dont_filter=False,
                                 )

    def parse(self, response, category=None, **kwargs):
        product_links = response.css(self.product_selector)
        yield from response.follow_all(product_links,
                                       callback=self.parse_product,
                                       cb_kwargs=dict(category=category))
        pagination_link = response.css(self.pagination_selector)
        yield from response.follow_all(pagination_link,
                                       callback=self.parse,
                                       cb_kwargs=dict(category=category))

    def parse_product(self, response, category):
        product_loader = ProductLoader(response=response)
        product_loader.add_value("category", category)
        product_loader.add_value("url", response.url)
        product_loader.add_css('name', self.name_selector)
        product_loader.add_css('reference', self.ref_selector)
        product_loader.add_css("image_url",  self.image_selector)
        product_loader.add_css("price",  self.price_selector)
        product_loader.add_css("description", self.specs_selector)
        yield product_loader.load_item()

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

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


