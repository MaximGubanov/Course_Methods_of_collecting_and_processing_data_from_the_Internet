import requests
from pprint import pprint

from lxml import html

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
URL = 'http://news.mail.ru'
response = requests.get(URL, headers=headers)

dom_news_links = html.fromstring(response.text)
news_links = dom_news_links.xpath("//div[@data-module='TrackBlocks']//a[contains(@class,'js-topnews__item') or contains(@class,'list__text')]/@href")
news_list = []

for url in news_links:
    r = requests.get(url, headers=headers)
    if r.ok:
        dom = html.fromstring(r.text)

        name = dom.xpath("//h1/text()")
        source_name = dom.xpath("//a[contains(@class, 'breadcrumbs__link')]/span/text()")
        datetime_at = dom.xpath("//span[@datetime]/@datetime")

        news = dict(name=name, link=url, source_name=source_name, datetime_at=datetime_at)
        news_list.append(news)

for row in news_list:
    row['datetime_at'] = row['datetime_at'][0].split('T')[0]
    row['source_name'] = row['source_name'][0]
    row['name'] = row['name'][0]

pprint(news_list)