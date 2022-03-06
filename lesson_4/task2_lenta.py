import requests
from pprint import pprint

from lxml import html

headers = {'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
URL = 'http://lenta.ru'
response = requests.get(URL, headers=headers)

dom = html.fromstring(response.text)
items = dom.xpath("//div[contains(@class, 'topnews')]")
items_list = []

for item in items:

    try:
        name = item.xpath("//a[contains(@class,'_topnews')]//h3/text()") \
            if item.xpath("//a[contains(@class,'_topnews')]//h3/text()") \
            else name = item.xpath("//span/text()")
    except (ValueError, AttributeError):
        name = ''

    link = dom.xpath("//a[contains(@class,'_topnews')]/@href")
    datetime_at = dom.xpath("//time/text()")

    dct = dict(name=name, link=link, datetime=datetime_at)
    items_list.append(dct)

pprint(items_list)