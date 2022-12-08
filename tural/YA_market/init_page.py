import multiprocessing as mp
import time
import os.path
import random
import pandas as pd
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
global name_html

url = 'https://partner.market.yandex.ru/welcome/exp/partners_2'
url_2 = 'https://partner.market.yandex.ru/business/1229830/assortment?campaignId=21656362&activeTab=offers&page=1&pageSize=100'
name_html = 'page_ya_lk.html'

def get_html(url,url_2):

    users = [{'http_proxy': '193.31.103.210:9244',
              'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'},
             {'http_proxy': '193.31.101.224:9604',
              'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.0.18635/886; U; en) Presto/2.4.15'},
             {'http_proxy': '193.31.102.78:9514',
              'user-agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.209.0 Safari/532.0'}]
    persona = random.choice(users)
    print(persona)

    # PROXY = persona['http_proxy']
    # webdriver.DesiredCapabilities.CHROME['proxy'] = {
    #     "httpProxy": PROXY,
    #     "ftpProxy": PROXY,
    #     "sslProxy": PROXY,
    #     "proxyType": "MANUAL",
    #
    # }
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True



    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={persona['user-agent']}")
    options.add_argument("--disable-blink-features=AutomationControlled")


    #options.add_argument(f"proxy-server={persona['http_proxy']}")

    s = Service(executable_path="C:/Users/venag/Downloads/chromedriver_win32/chromedriver.exe")

    driver = webdriver.Chrome(options=options, service=s)
    driver.get(url)
    time.sleep(20)


    #driver.by_class_name("lc-button__under").click
    #time.sleep(10)
    driver.get(url_2)


    for i in range(22):
        time.sleep(20)
        html = driver.page_source
        if i < 9:
            k = '0'
        else:
            k = ''
        with open('pages/' + 'говоно_yandex_market_'+k+str(i+1)+'.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('Страница готова ',i+1)


    driver.close()
    driver.quit()



if __name__ == '__main__':
    get_html(url,url_2)




