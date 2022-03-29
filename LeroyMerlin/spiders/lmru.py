import scrapy
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from LeroyMerlin.items import LeroyMerlinItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://leroymerlin.ru/search/?q={kwargs.get('search')}"]

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyMerlinItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("name", "//h1[@slot='title']/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath("photos", "//img[@slot='thumbs']/@src")
        yield loader.load_item()

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)