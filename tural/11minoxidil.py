from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from openpyxl.workbook import Workbook
import re

name = '11minoxidil.ru'

list_url = ['https://11minoxidil.ru/katalog-tovarov/xinoxin',
            'https://11minoxidil.ru/katalog-tovarov/minoksidil-5']

df = pd.DataFrame(columns=['name','price','obem','price_before','proizvpditel','country','nalichie', 'url'])

def parsing_kategory(url):
    link = url
    response = requests.get(link).text
    soup = BS(response, "lxml")

    soup = soup.find('div', class_="row js_catalog-wrap js_show-more-main-wrap")
    internalLinks = [a.get('href') for a in soup.find_all('a') if a.get('href') and a.get('href').startswith('/')]
    return internalLinks


url_all = []
for url in list_url:
    url_all = url_all + parsing_kategory(url)

url_all = list(set(url_all))
url_all = ['https://11minoxidil.ru' + url_1 for url_1 in url_all]
print(url_all)
print(len(url_all))


def parsing_each_url(url):
    link_2 = url
    response = requests.get(link_2).text
    soup = BS(response, "lxml")
    box = 'item-block-right-inner'

    name = soup.find('h1').text.strip()

    price = soup.find('div', {'class': box}).find(class_="price__current").text.strip().replace(' ', '')
    price = re.sub(r'\W+', '', price)[:-1]

    v = ''
    try:
        v = soup.find('div', {'class': box}).find(
            class_="item-block-right__volume item-block-right__text").text.strip().replace(' ', '')
    except:
        pass

    price_before = ''
    try:
        price_before = soup.find('div', {'class': box}).find(class_="price__before thro").text.strip()
        price_before = re.sub(r'\W+', '', price_before)[:-1]
    except:
        pass

    nalichie = ''
    try:
        nalichie = soup.find('div', {'class': box}).find(class_="item-block-right__action").text.strip()
        # price_before = re.sub(r'\W+', '', price_before)[:-1]
        if nalichie == 'В корзину':
            nalichie = 'В наличие'
        else:
            nalichie = 'Нет'
    except:
        pass

    proizvpditel = ''
    try:
        proizvpditel = soup.find('div', {'class': box}).find(
            class_="item-block-right__brend item-block-right__text").text
        proizvpditel = re.sub(r'\W+', ' ', proizvpditel).replace("Производитель", "").strip()
    except:
        pass

    country = soup.find('div', {'class': box}).find(class_="item-block-right__country item-block-right__text").text
    country = re.sub(r'\W+', '', country).replace("Страна", "")

    url = url
    return (name, price, v, price_before, proizvpditel, country, nalichie, url)

for url in url_all:
    name,price,v,price_before,proizvpditel,country,nalichie,url = parsing_each_url(url)
    df = df.append({'name': name, 'price': price, 'obem': v, 'price_before': price_before, 'proizvpditel': proizvpditel,
                'country': country, 'nalichie': nalichie, 'url': url}, ignore_index=True)




print(df)


writer = ExcelWriter('fucking_parsing.xlsx')
df.to_excel(writer, index = False)
writer.save()


