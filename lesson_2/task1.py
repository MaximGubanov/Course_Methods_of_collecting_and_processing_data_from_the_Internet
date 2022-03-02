from pymongo import MongoClient

from get_content import get_content_page


def save_db(parsed_data):

    for data in parsed_data:

        _id = vacancy.count_documents({})
        res = vacancy.count_documents(data)

        if res >= 1:
            # print(vac)
            continue
        else:
            data['_id'] = _id + 1
            vacancy.insert_one(data)


if __name__ == '__main__':

    client = MongoClient('127.0.0.1', 27017)
    db = client['vacancies']
    vacancy = db.vacancy

    vacancy.delete_many({})
    vacancies = get_content_page(search_param='python')
    save_db(vacancies[0])   # ф-я get_content_page возвращает кортеж из трёх эл-ов, но в данном случае нам интересен
                            # только нулевой индекс - тело контента

    for vac in vacancy.find({}):
        print(vac)