import multiprocessing as mp
import time
import re
import os.path
import random
import pandas as pd
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
import lib.headers

start_time = time.time()

all_url = ['https://www.wildberries.ru/catalog/102240137/detail.aspx?targetUrl=GP',
           'https://www.wildberries.ru/catalog/119968817/detail.aspx?targetUrl=GP']
from links_for_parsing import file_url
all_url = file_url

global filename, image_path, driver
filename = r'C:\PyProjects\poject_1\tural\new_wb_pars\wildberries_nalichie_all.xlsx'
image_path = r'C:\PyProjects\poject_1\tural\new_wb_pars\images\phone'


def get_html(url):

    users = [{'http_proxy': '193.31.103.210:9244',
              'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'},
             {'http_proxy': '193.31.101.224:9604',
              'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.0.18635/886; U; en) Presto/2.4.15'},
             {'http_proxy': '193.31.102.78:9514',
              'user-agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.209.0 Safari/532.0'}]
    persona = random.choice(users)


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
        driver.request_interceptor = lib.headers.interceptor
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "collapsible__toggle-wrap")))
            html = driver.page_source
        except:
            html = driver.page_source
    except Exception as ex:
        print('Cсылка не выполнилась')
        print(url)
        html = None
    finally:
        driver.close()
        driver.quit()
        time.sleep(3)
    return html


def parse_data(html):

    soup = BeautifulSoup(html, 'html.parser')
    try:
        price = get_price(soup)
    except:
        return 'error'
    if price == 'Не найдена':
        return 'Не найдена'
    else:
        try:
            price = re.findall(r'[0-9]+', re.sub(r'\xa0', '', price))[0] if price else None
        except:
            price = 0
        return price


def write_to_csv(row,df):
    if os.path.isfile(filename):
        wb = load_workbook(filename)
        sheet = wb.active
        sheet.append(row)
        wb.save(filename)
    else:
        df.to_excel(filename, index = False)


def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
        except:
            data = None
        return data
    return wrapper

@try_except
def get_price(soup):
    if soup.h1.string == 'По Вашему запросу ничего не найдено':
        return 'Не найдена'
    else:
        return soup.find('ins', attrs={'class': 'price-block__final-price'}).get_text()



def save_df(df):
    #filename = 'wildberries_data.csv'
    if os.path.isfile(filename):
       print('Удали файл')
    else:
        df.to_excel(filename, index = False)



if __name__ == '__main__':



    df = pd.DataFrame(columns=['Цена до скидки','url'])

    p = mp.Pool(processes=10)

    html = p.map(get_html, all_url[:300])
    print('part 1 end')
    time.sleep(60)
    html += p.map(get_html, all_url[300:600])
    print('part 2 end')
    time.sleep(60)
    html += p.map(get_html, all_url[600:900])
    print('part 3 end')
    time.sleep(60)
    html += p.map(get_html, all_url[900:1200])
    print('part 4 end')
    time.sleep(60)
    html += p.map(get_html, all_url[1200:])
    print('part 5 end')

    print("--- %s seconds ---" % (time.time() - start_time))
    j = 0
    for i in html:

        price = parse_data(i)

        row = (price, all_url[j])
        df.loc[j] = row
        j += 1

    save_df(df)
    print("--- %s seconds ---" % (time.time() - start_time))
