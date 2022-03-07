import requests
from pprint import pprint

from lxml import html

headers = {'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
URL = 'http://lenta.ru'
response = requests.get(URL, headers=headers)

dom = html.fromstring(response.text)
items = dom.xpath("//div[contains(@class, 'topnews__column')]")
items_list = []

for item in items:
    """Илья, в чем у меня ошибка? Я проставил точки перед xml запросами, а у меня все равно конечный список словарей
    формируется не правильно"""
    name = item.xpath(".//a//span/text()")
    link = dom.xpath(".//a[contains(@class, '_topnews')]/@href")
    datetime_at = dom.xpath(".//a//time/text()")

    dct = dict(name=name, link=link, datetime=datetime_at)
    items_list.append(dct)

pprint(items_list)