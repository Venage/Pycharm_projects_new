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


start_time = time.time()

url = 'https://market.csgo.com/item/3757781165'


filename = r'C:\PyProjects\poject_1\tural\new_wb_pars\wildberries_url_on.xlsx'



global driver


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
        #driver.request_interceptor = lib.headers.interceptor
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



def parse_data(html):

    soup = BeautifulSoup(html, 'html.parser')

    all_href = soup.find('div', attrs={'class': 'product-card-overflow'}).find_all('a', href=True)
    soup = str(all_href).replace('="', '99999')  # .replace('">','99999')
    soup = soup.replace('">', '99999')
    soup = soup.replace(' ', '99999')
    soup = soup.replace('switches', '99999')
    soup = soup.replace('new', '99999')
    soup = soup.replace('part', '99999')
    soup = soup.split('99999')

    internalLinks = []
    for i in soup:
        if len(i) > 45:
            internalLinks.append(i)
    return internalLinks


if __name__ == '__main__':

    #p = mp.Pool(processes=10)
    #html = p.map(get_html, all_url)
    html = get_html(url)
    print(html)




    print("--- %s seconds ---" % (time.time() - start_time))
