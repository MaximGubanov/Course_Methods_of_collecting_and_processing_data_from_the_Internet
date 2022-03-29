from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from LeroyMerlin import settings
from LeroyMerlin.spiders.lmru import LmruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmruSpider, search='DEXTER')

    process.start()