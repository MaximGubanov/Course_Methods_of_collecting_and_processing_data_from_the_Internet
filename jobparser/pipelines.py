# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy1803

    def _salary_parse(self, data):
        """если в data нет данных по ЗП, то буду считать, что ЗП не указана. Иногда data равна всего одному значению -
        [по договорённости] или [ЗП не указана]"""
        if len(data) == 1 or data is None:
            return dict(min_salary=None, max_salary=None, valuta=None)

        """тут просто избавляюсь от '\xa0' """
        data = list(map(lambda x: x.replace('\xa0', '').strip(), data))

        valuta = 'USD' if 'USD' in data else 'RUB'

        s = []  # тут собираются числа по ЗП, либо один, либа два числа

        """делаю проход по спску, если len(data) больше одного"""
        for item in data:
            """если в цикле собрали уже два чила, то это и сеть salary_min и salary_max. Выходим из ф-и, т.к. дальше 
            нет смысла обходить список"""
            if len(s) == 2:
                return dict(min_salary=s[0], max_salary=s[1], valuta=valuta)

            try:
                """если значение можно привести к числу, то приводим его в int и добавляем в наш список s = [] """
                s.append(int(item))
                continue
            except Exception:
                """иначе пробуем распарсить такие значения, например как '100000руб' """
                result = []
                for symbol in item:
                    try:
                        el = list(filter(lambda x: x in '0123456789', symbol))[0]
                        result.append(el)
                    except Exception:
                        continue
                if len(result) == 0:
                    continue
                else:
                    """если все успешно, то добавляем число в s = [] """
                    s.append(int(''.join(result)))

        """тут определяем тип списка, когда значение ЗП всего одно, чтобы понять где salary_min, а где salary_max """
        if 'от' in data:
            return dict(min_salary=s[0], max_salary=None, valuta=valuta)
        if 'до' in data:
            return dict(min_salary=None, max_salary=s[0], valuta=valuta)

    def process_item(self, item, spider):
        # Отправляю значение ключа salary на обработку
        item['salary'] = self._salary_parse(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item