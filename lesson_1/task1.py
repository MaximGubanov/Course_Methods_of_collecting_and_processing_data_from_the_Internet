import requests
import json
from tabulate import tabulate

URL = 'https://api.github.com/users/MaximGubanov/repos'
HEADERS = {'Accept': 'application/vnd.github.v3+json'}


def get_content(url, headers):
    response = requests.get(url, headers=headers)
    json_data = response.json()
    return json_data


def parse_repo(data):
    """Ф-я генерирует и возвращает кортеж из 2-х словарей
    dict_for_tabulate - это просто для красивого вывода в print
    dict_for_json - для сохранения в JSON """

    dict_for_tabulate = {'№': [], 'Name repository': [], 'Created_at': []}
    dict_for_json = {}

    for num, repo in enumerate(data, 1):

        dict_for_tabulate['№'].append(num)
        dict_for_tabulate['Name repository'].append(repo.get('name'))
        dict_for_tabulate['Created_at'].append(repo.get('created_at').replace('T', '  '))

        dict_for_json[num] = dict(Name=repo.get('name'), Created_at=repo.get('created_at'))

    return (dict_for_tabulate, dict_for_json)


def save_json(print_tab, data):
    """Ф-я сохраняет в JSON-файл и выводит print через модуль tabulate"""

    with open('task1.json', 'w', encoding='utf-8') as whrite_file:
        json.dump(data, whrite_file, indent=4)

    print(tabulate(print_tab, headers='keys', tablefmt='grid'))


if __name__ == '__main__':

    content_data = get_content(URL, HEADERS)
    print_tabulate, dict_data = parse_repo(content_data)
    save_json(print_tabulate, dict_data)