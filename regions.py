import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd


page = r.get('http://www.statdata.ru/spisok-regionov-rossii-s-kodamy').content
obl = list()
page = bs(page, 'lxml')

line_obls = page.find('div', id='sites-canvas').find('table').find('table').find('tbody').find_all('tr')
for oblas in line_obls:
    obl.append(oblas.find_all('td')[1].text)
print(obl[1:])

df = pd.DataFrame({
    'Облать': obl[1:]
})

df.to_csv('regions.csv')