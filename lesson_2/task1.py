#https://nn.hh.ru/search/vacancy?area=113&professional_role=96&search_field=name&search_field=company_name&search_field=description&text=Python
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json


def parse_salary(data):
    """Ф-я парсит поле оплаты труда и возвращает строку или None"""
    if data is not None:
        data = data.split(' ')
        valuta = data.pop(-1)
        salary_dict = {'min': None, 'max': None, 'valuta': valuta}
        salary_list = []
        if 'от' in data:
            salary_dict['min'] = int(data[1].replace('\u202f', ''))
            return salary_dict
        if 'до' in data:
            salary_dict['max'] = int(data[1].replace('\u202f', ''))
            return salary_dict

        for pos in data:
            try:
                pos_ = int(pos.replace('\u202f', ''))
                salary_list.append(pos_)
            except ValueError:
                continue
        return dict(min_salary=salary_list[0], max_salary=salary_list[1], valuta=valuta)

    return dict(min_salary=None, max_salary=None, valuta=None)


def parse_page(vacancies):

    vacancies_list_page = []

    for vacancy in vacancies:
        vacancy_data = {}
        name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()

        try:
            salary_data = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
        except AttributeError:
            salary_data = None

        salary_ = parse_salary(salary_data)
        vacancy_data['name_vacancy'] = name
        vacancy_data['salary'] = salary_
        vacancies_list_page.append(vacancy_data)

    return (vacancies_list_page, len(vacancies))


def get_content_page(search_param, page_next=True):
    base_url = 'https://nn.hh.ru/'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/98.0.4758.102 Safari/537.36'}
    params = {'text': search_param,
              'page': 0}
    url = f'{base_url}search/vacancy?area=113&professional_role=96&search_field=name&search_field=' \
          f'company_name&search_field=description&'

    count = 0
    pages = []

    while page_next is not None:
        response = requests.get(url, headers=headers, params=params)
        dom = BeautifulSoup(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
        page_next = dom.find('a', {'data-qa': 'pager-next'})
        parsed_page, count_vac = parse_page(vacancies)
        pages += parsed_page
        count += count_vac
        params['page'] += 1

    return (pages, params['page'], count)


if __name__ == '__main__':
    all_vacancies, count_pages, count_vacancies = get_content_page(search_param='python')
    pprint(all_vacancies)
    print('======================================================================')
    print(f'Найдено {count_vacancies} вакансий на {count_pages} страницах')

    with open('result.json', 'a+', encoding='utf-8') as whrite_f:
        json.dump(all_vacancies, whrite_f, indent=4)