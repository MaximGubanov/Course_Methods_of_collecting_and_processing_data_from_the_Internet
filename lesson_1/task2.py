"""Этот API предназначен для сбора данных изображений, собранных марсоходами НАСА Curiosity, Opportunity и Spirit,
и делает их более доступными для других разработчиков, преподавателей и гражданских ученых.
"""
import json
import requests

URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&page=2&api_key=" \
      "elO9A3mHFkGIGYo6vGIwnzawrg6FjgtlzEg1ojJf"

URL1 = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=" \
       "elO9A3mHFkGIGYo6vGIwnzawrg6FjgtlzEg1ojJf"

response = requests.get(URL1)

data = response.json()

for row in data['photos']:
    print(row['img_src'])

with open('task2-1.json', 'w') as whrite_file:
    json.dump(data, whrite_file, indent=2)
