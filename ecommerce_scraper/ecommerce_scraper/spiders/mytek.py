
import scrapy
from ..items import LaptopItem

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class MytekSpider(scrapy.Spider):
    """
    Spider class that crawls websites similar to mytek.com
    """

    def start_requests(self):
        for u, cat, meth in zip(self.urls, self.categories, self.parse_methods):
            yield scrapy.Request(u, callback="parse",
                                 cb_kwargs=dict(category=cat, parse_method=meth),
                                 errback=self.errback_httpbin,
                                 dont_filter=False)

    def parse(self, response, category=None, parse_method=None, **kwargs):
        product_links = response.css(self.product_selector)
        yield from response.follow_all(product_links,
                                       callback=getattr(self, parse_method),
                                       cb_kwargs=dict(category=category))
        pagination_link = response.css(self.pagination_selector)
        yield from response.follow_all(pagination_link,
                                       callback=self.parse,
                                       cb_kwargs=dict(category=category, parse_method=parse_method))

    def parse_laptop(self, response, category=None):
        laptop = LaptopItem()
        laptop["category"] = category
        laptop["url"] = response.url
        specs = response.css(self.laptop_specs_selector)
        for field in laptop:
            laptop[field] = specs.re(getattr(self, f'{field}_pattern'))
        yield laptop


        # laptop['name'] = self.get_item_field(response, self.name_selector, '::text', self.name_re)
        # laptop['price'] = self.get_item_field(response, self.price_selector, '::text', self.price_re)
        # laptop['reference'] = self.get_item_field(response, self.ref_selector, '::text', self.ref_re)
        # laptop['category'] = category
        # laptop['url'] = response.url
        # laptop['state'] = self.get_item_field(response, self.state_selector, '::text', self.state_re)
        # laptop['discount'] = self.get_item_field(response, self.discount_selector, '::text', self.discount_re)
        # laptop['warranty'] = self.get_item_field(response, self.warranty_selector, '::text', self.warranty_re)
        # laptop['image'] = self.get_item_field(response, self.image_selector, '::attr(href)')
        #
        # laptop['os'] = self.get_item_field(response, self.os_selector, '::text', self.os_re)
        # laptop['processor'] = self.get_item_field(response, self.proc_selector, '::text', self.proc_re)
        # laptop['processor_frequency'] = self.get_item_field(response, self.proc_freq_selector, '::text', self.proc_freq_re)
        # laptop['core_type'] = self.get_item_field(response, self.core_type_selector, '::text', self.core_type_re)
        # laptop['cache'] = self.get_item_field(response, self.cache_selector, '::text', self.cache_re)
        # laptop['ram'] = self.get_item_field(response, self.ram_selector, '::text', self.ram_re)
        # laptop['ram_frequency'] = self.get_item_field(response, self.ram_freq_selector, '::text', self.ram_freq_re)
        # laptop['screen_size'] = self.get_item_field(response, self.screen_size_selector, '::text', self.screen_size_re)
        # laptop['screen_resolution'] = self.get_item_field(response, self.screen_res_selector, '::text', self.screen_res_re)
        # laptop['touch_screen'] = self.get_item_field(response, self.touch_screen_selector, '::text', self.touch_screen_re)
        # laptop['hard_disk'] = self.get_item_field(response, self.hd_selector, '::text', self.hd_re)
        # laptop['graphics_card'] = self.get_item_field(response, self.graphics_card_selector, '::text', self.graphics_card_re)
        # laptop['connections'] = self.get_item_field(response, self.connect_selector, '::text', self.connect_re)
        # laptop['bluetooth'] = self.get_item_field(response, self.bluetooth_selector, '::text', self.bluetooth_re)
        # laptop['color'] = self.get_item_field(response, self.color_selector, '::text', self.color_re)




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
