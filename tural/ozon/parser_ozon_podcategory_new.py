import multiprocessing as mp
import time
import re
import os.path
import random
import pandas as pd
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_product import UseSelenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
import lib_2.headers
import json
import glob
import ast
global driver,class_in_page

start_time = time.time()

all_url = 'https://www.ozon.ru/category/fotoramki-i-fotoalbomy-14637/'
class_in_page = 'widget-search-result-container ku5'



def get_html(url):

    users = [{'http_proxy': '193.31.103.210:9244',
              'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'},
             {'http_proxy': '193.31.101.224:9604',
              'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.0.18635/886; U; en) Presto/2.4.15'},
             {'http_proxy': '193.31.102.78:9514',
              'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}]
    persona = random.choice(users)
    print(persona)

    PROXY = persona['http_proxy']
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",

    }
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True



    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={persona['user-agent']}")
    options.add_argument("--disable-blink-features=AutomationControlled")


    #options.add_argument(f"proxy-server={persona['http_proxy']}")

    s = Service(executable_path="C:/Users/venag/Downloads/chromedriver_win32/chromedriver.exe")

    driver = webdriver.Chrome(options=options, service=s)

    try:
        driver.request_interceptor = lib_2.headers.interceptor
        driver.get(url)
        #wait = WebDriverWait(driver, 5)
        time.sleep(5)
        #wait.until(EC.presence_of_element_located((By.CLASS_NAME, "collapsible__toggle-wrap")))
        html = driver.page_source
    except:
        html = None
    finally:
        driver.close()
        driver.quit()
    return html


def parse_data(html,class_in_page):

    soup = BeautifulSoup(html, 'html.parser')

    all_href = soup.find('div', attrs={'class': f'{class_in_page}'}).find_all('a')

    list_name = []
    for i in all_href:
        if i['href'] not in list_name:
            list_name.append(i['href'].partition('?')[0])

    return list_name

def obrabotka_url(new_urls_1):
    json_url_list = []
    for url in new_urls_1:
        json_url_list.append('https://www.ozon.ru/api/composer-api.bx/page/json/v2'+'?url='+url)
    return json_url_list


def parse_data_info(data: dict) -> dict:
    widgets = data.get('widgetStates')
    for key, value in widgets.items():
        if 'webProductHeading' in key:
            title = json.loads(value).get('title')
        if 'webSale' in key:
            prices = json.loads(value).get('offers')[0]
            if prices.get('price'):
                price = re.search(r'[0-9]+', prices.get('price').replace(u'\u2009', ''))[0]
            else:
                price = 0
            if prices.get('originalPrice'):
                discount_price = re.search(r'[0-9]+', prices.get('originalPrice').replace(u'\u2009', ''))[0]
            else:
                discount_price = 0
        if 'webGallery' in key:
            url_pic = json.loads(value).get('coverImage')

    layout = json.loads(data.get('layoutTrackingInfo'))
    brand = layout.get('brandName')
    category = layout.get('categoryName')
    sku = layout.get('sku')
    url = layout.get('currentPageUrl')


    product = {
        'title': title,
        'price': price,
        'discount_price': discount_price,
        'brand': brand,
        'category': category,
        'sku': sku,
        'url': url,
        'url_pic': url_pic
    }
    return product

def save_url_file(product: str, i: int, filename: str) -> None:
    url = 'https://www.ozon.ru/api/composer-api.bx/page/json/v2' \
          f'?url={product}'
    filename = filename + str(i) + '.html'
    UseSelenium(url, filename).save_page()

def get_products() -> list:
    return glob.glob('products/*.html')

def get_json(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
        return json.loads(data)



if __name__ == '__main__':
    html = get_html(all_url)

    new_urls_1 = parse_data(html,class_in_page)
    new_urls_1 = new_urls_1[::2]
    new_urls_1 = new_urls_1[:10]

    json_url_list = obrabotka_url(new_urls_1)

    #json_str = p.map(get_html, json_url_list)
    i = 1
    for product in json_url_list:
        save_url_file(product, i, filename='product_')
        i += 1

    products = get_products()
    df_all = pd.DataFrame(columns=['title', 'price', 'discount_price', 'brand', 'category', 'sku', 'url', 'url_pic'])
    i = 0
    # for product in products:
    #     try:
    #         product_json = get_json(product)
    #         result = parse_data_info(product_json)
    #         df_all.loc[i] = list(result.values())
    #     except Exception as e:
    #         print(e)
    #     i += 1
    #
    # print(df_all)
    print(json_url_list[0])
    #print(get_json(products[0]))

    # i = 0
    # for product in json_str:
    #     try:
    #         result = parse_data_info(json.loads(product)) #преобразование str в json
    #         df_all.loc[i] = list(result.values())
    #     except Exception as e:
    #         print(e)
    #     i+=1
    #
    # print(df_all)


print("--- %s seconds ---" % (time.time() - start_time))
