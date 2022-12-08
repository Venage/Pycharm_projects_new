from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pathlib import Path
from openpyxl.workbook import Workbook

pyt_misha = 'A:/tural'
pyt_tural = 'F:/karnaval'

if Path('A:/tural').is_dir() == True:
    pyt = pyt_misha
else:
    pyt = pyt_tural

name = 'minoxidil4you'
link = "https://minoxidil4you.ru/catalog/minoxidil-dlya-volos/"
response = requests.get(link).text
soup = BS(response, "lxml")


title_all = soup.find('div', {'class': 'b-catalog-section'}).find_all(class_="b-catalog-section__item-name")
price = soup.find('div', {'class': 'b-catalog-section'}).find_all(itemprop="price")
#print(title_all[0].text)
#print(price[0].get('content'))

fake_price = []
real_price = []
title = []

for i,j in zip(price,title_all):
    real_price.append(i.get('content'))
    title.append(j.text.strip())

#print(title)


columns = ['Товар', 'Реальная_цена']
data = [title,real_price]
data = np.array([title,real_price])
data = data.transpose()


df = pd.DataFrame(data = data, columns = columns)
df['Фирма'] = name
print(df)





writer = ExcelWriter(f'{pyt}/parsing_{name}.xlsx')
df.to_excel(writer, index = False)
writer.save()