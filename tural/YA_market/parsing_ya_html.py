import time
from bs4 import BeautifulSoup
import multiprocessing as mp
import os
import json
import re
import pandas as pd
import requests
import openpyxl.drawing.image
from PIL import Image as pilIm
from openpyxl import load_workbook
import shutil
import glob
start_time = time.time()


file_name = r'C:\PyProjects\poject_1\tural\YA_market\YA_parsing.xlsx'



def get_pages() -> list:
    #return glob.glob(os.getcwd()+'/pages/*.html')
    return glob.glob('C:/PyProjects/poject_1/tural/YA_market/pages/*.html')

def get_html(page: str):
    with open(page, 'r', encoding='utf-8') as f:
        return f.read()

def get_info(html):

    soup = BeautifulSoup(html, 'html.parser')

    sku_all = pars_sku(soup)
    name_all = pars_name(soup)
    url_all = pars_url(soup)
    price_all = pars_price(soup)
    color_all = pars_color(soup)

    product = {
        'sku': sku_all,
        'name': name_all,
        'url': url_all,
        'price' : price_all,
        'color' : color_all
    }
    print(len(sku_all))
    print(len(name_all))
    print(len(url_all))
    print(len(price_all))
    print(len(color_all))

    return product

#----------------------------------------------------------------------------------------------------------
def pars_sku(soup):
    try:
        sku_all = []
        sku_all_soup = soup.find_all('span', attrs={'data-e2e': 'offer-id'})
        for sku in sku_all_soup:
            sku_all.append(sku.get_text())
    except:
        sku_all = ''
    return sku_all

def pars_name(soup):
    try:
        name_all = []
        name_all_soup = soup.find('tbody', attrs={'class': '___tbody___N4suF style-tBody___w0RYe'} ).\
            find_all('div', attrs={'class': 'style-root___nZXUK'})
        for name in name_all_soup:
            try:
                name_all.append(name.find('a', attrs={'class': '___Clickable___fcJVD style-link___h32hY'}).get_text())
            except:
                name_all.append('')
    except:
        name_all = ''
    return name_all

def pars_url(soup):
    try:
        url_all = []
        url_all_soup = soup.find('tbody', attrs={'class': '___tbody___N4suF style-tBody___w0RYe'} ). \
            find_all('div', attrs={'class': 'style-root___nZXUK'})
        for url in url_all_soup:
            try:
                url_all.append('https://partner.market.yandex.ru'+url.find('a', attrs={'class': '___Clickable___fcJVD style-link___h32hY'}).get('href'))
            except:
                url_all.append('')
    except:
        url_all = ''
    return url_all


def pars_price(soup):
    price_all = []
    try:
        price_all_soup = soup.find_all('tr', attrs={'class': '___tr___z6ZcU style-row___szOkl'})
        for i in price_all_soup:
            try:
                price = i.find_all('div', attrs={'class': '___Tag___xFCxD __use--kind___TqC3g __use--kind_tableBody____vp1n'})[-1].get_text()
                price_all.append(price.replace('\xa0','').replace(' ₽',''))
            except:
                price_all.append(" ")
    except:
        price_all = ''
    return price_all


def pars_color(soup):
    try:
        color_all = []
        color_all_soup = soup.find_all('tr', attrs={'class': '___tr___z6ZcU style-row___szOkl'})

        color_status = []
        for link in color_all_soup:
            try:
                color = link.find_all('div', attrs={'class': '___container___BOaT4 __use--size___UTdTw __use--size_s___RqL7v __use--shape___IT5iw __use--shape_rounded___jCKOb'})[1].get('style')

                    # Желтые
                if color in ['background-color: rgb(255, 236, 204);']:
                    color_status.append('Товар скрыт или его нет на складе')
                    # Зеленые
                elif color in ['background-color: rgb(42, 173, 46);', 'background-color: rgb(223, 244, 217);']:
                    color_status.append('Размещен')
                    # Красные
                elif color in ['background-color: rgb(255, 0, 0);','background-color: rgb(255, 224, 224);']:
                    color_status.append('При размещении возникли ошибки')
                else:
                    color_status.append('Готов к размещению')
            except:
                color_status.append('')

        # print(color_all_soup)
        # for color in color_all_soup:
        #     try:
        #         color
        #         color_all.append(color.get('style')) #.replace(': ','99999').replace('; ','99999').split('99999')[3])
        #     except:
        #         color_all.append('')
        # color_status = []
        # for i in color_all:
        #     if i == 'rgb(255, 162, 0)':
        #         color_status.append('Товар скрыт или его нет на складе')
        #     elif i == 'rgb(42, 173, 46)':
        #         color_status.append('Размещен')
        #     elif i == 'rgb(255, 0, 0)':
        #         color_status.append('При размещении возникли ошибки')
    except:
        color_status = ''
    return color_status
#----------------------------------------------------------------------------------------------------------
def html_product(pages):
    html = get_html(pages)
    product = get_info(html)
    return product


if __name__ == '__main__':
    pages = get_pages()

    df_all = pd.DataFrame(columns=['sku','name','url','price','color','file'])

    i = 0
    for page in pages:
        i +=1
        try:
            product = html_product(page)
            df_new = pd.DataFrame.from_dict(product)
            df_new['file'] = page
            df_all = df_all.append(df_new, ignore_index=True)
            print(i)
        except:
            pass

    df_all.to_excel(file_name, index = False)



    # print(pages[1])
    # j = 1
    # for i in product['color']:
    #     print(j,' ', i)
    #     j+=1

    print(df_all)
    print("--- %s seconds ---" % (time.time() - start_time))