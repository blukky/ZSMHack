import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import re

country = list()
obl = list()
photo = list()

page = r.get('https://ruralisation.ru/krasivie-derevni').content

page = bs(page, 'lxml')

page2 = r.get('https://ruralisation.ru/krasivie-derevni?start=16').content

page2 = bs(page2, 'lxml')

page3 = r.get('https://ruralisation.ru/krasivie-derevni?start=32').content

page3 = bs(page3, 'lxml')

items1 = page.find_all('div', class_='rur_blog_item')
items2 = page2.find_all('div', class_='rur_blog_item')
items3 = page3.find_all('div', class_='rur_blog_item')

items = items1 + items2 + items3

for item in items:
    country.append(re.sub(r"[\n\t]", "", item.find('div', class_='rur_blog_item_project_name').text))
    obl.append(re.sub(r"[\n\t, ]", "", item.find('div', class_='rur_blog_item_project_addr').text))
    photo.append('https://ruralisation.ru' + item.find('div', class_='rur_blog_item_img').get('style').split("(")[1])

# page = r.get('https://ruralisation.ru/villages/').content
#
# page = bs(page,'lxml')
#
# items = page.find_all('div', class_='village_item')
# items = items[:2] + items[3:]
# print(len(items))
# country = list()
# obl = list()
# photo = list()
# for item in items:
#     print(item.find('div', class_='village_item_desc').find('h4').text)
#     print(item.find('div', class_='village_item_desc').find('p').text)
#     print('https://ruralisation.ru/villages/'+ item.find('img').get('src'))
#     country.append(item.find('div', class_='village_item_desc').find('h4').text)
#     obl.append(item.find('div', class_='village_item_desc').find('p').text)
#     photo.append('https://ruralisation.ru/villages/'+ item.find('img').get('src'))

df = pd.DataFrame({
    'Деревня': country,
    "Область": obl,
    'Фотография': photo
})

df.to_csv('Красивые деревни.csv')
