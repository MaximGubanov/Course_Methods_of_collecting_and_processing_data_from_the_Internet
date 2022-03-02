from pymongo import MongoClient
from pprint import pprint


def search_salary(value, valuta):

    for row in vacancy.find({
        '$and': [{'salary.valuta': valuta},
                {'$or': [
                    {'salary.min_salary': {'$gte': value}},
                    {'salary.max_salary': {'$gte': value}}]}]}):

        pprint(row)


if __name__ == '__main__':
    client = MongoClient('127.0.0.1', 27017)
    db = client['vacancies']
    vacancy = db.vacancy

    search_salary(value=50000, valuta='RUB')  # у валюты есть два значение: 'RUB' или 'USD'