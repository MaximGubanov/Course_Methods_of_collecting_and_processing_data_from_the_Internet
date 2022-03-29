# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose
from twisted.web.html import output


def clear_price(value):
    value = value.replace('\xa0', '')
    try:
        value = int(value)
    except Exception as e:
        print(e)
        return value
    return value


def change_link(link: str):
    try:
        return link.replace('w_82,h_82', 'w_500,h_500')
    except Exception as e:
        return e


class LeroyMerlinItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=Compose(change_link), output_processor=TakeFirst())
    _id = scrapy.Field()