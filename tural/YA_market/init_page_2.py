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
from selenium.webdriver.common.action_chains import ActionChains
global name_html,login_ya,password_ya,url_ya_log_pas

url_ya_log_pas = 'https://passport.yandex.ru/auth?retpath=https%3A%2F%2Fpartner.market.yandex.ru%2Fbusinesses'
url_2_tural_shop = 'https://partner.market.yandex.ru/business/1229830/assortment?campaignId=21656362&activeTab=offers&page=1&pageSize=100'
name_html = 'page_ya_'
login_ya = 'turalbahshaliev@yandex.ru'
password_ya = '281832klmnopQ'

def fun_login_ya():
    users = [{'http_proxy': '193.31.103.210:9244',
              'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.0.18635/886; U; en) Presto/2.4.15'},
             {'http_proxy': '193.31.101.224:9604',
              'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.0.18635/886; U; en) Presto/2.4.15'},
             {'http_proxy': '193.31.102.78:9514',
              'user-agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/5.0.18635/886; U; en) Presto/2.4.15'}]
    persona = random.choice(users)
    print(persona)


    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={persona['user-agent']}")
    options.add_argument("--disable-blink-features=AutomationControlled")


    s = Service(executable_path="C:/Users/venag/Downloads/chromedriver_win32/chromedriver.exe")

    driver = webdriver.Chrome(options=options, service=s)
    driver.set_window_size(1000, 1000)
    driver.get(url_ya_log_pas)

    time.sleep(3)
    email_inpit = driver.find_element('id','login')
    email_inpit.clear()
    email_inpit.send_keys(login_ya)
    time.sleep(2)

    password_inpit = driver.find_element('id','passwd')
    password_inpit.clear()
    password_inpit.send_keys(password_ya)
    time.sleep(2)
    # login_button = driver.find_element('passp:sign-in').click()
    # time.sleep(2)
    # login_button_2 = driver.find_element('passp:sign-in').click()
    # time.sleep(2)

    LOGIN_BUTTON_XPATH = '//button[@type="submit"]'  # открывающий тег и любое уникальное название
    driver.find_element(by=By.XPATH, value=LOGIN_BUTTON_XPATH).click()
    time.sleep(10)
    return driver




#next_page_button = driver.find_element('data-tid','2c3a30f5 890bc542').click()
def load_html_ya(driver):
    driver.get(url_2_tural_shop)

    for i in range(30):
        driver.execute_script("window.scrollTo(0, 100000)")
        time.sleep(15)
        html = driver.page_source
        if i < 9:
            k = '0'
        else:
            k = ''
        with open('pages/' + name_html + k + str(i + 1) + '.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('Страница готова ', i + 1)
        time.sleep(4)
        try:
            NEXT_BUTTON_XPATH = '//button[@icon="chevronRight"]'
            driver.find_element(by=By.XPATH, value=NEXT_BUTTON_XPATH).click()
        except:
            break
        # driver.execute_script("window.scrollTo(0, 100000)")
        # ActionChains(driver).reset_actions()
        # ActionChains(driver).move_by_offset(667, 800).click().perform()
    print('='*50)
    print(f'Страницы 1 - {i+1} готовы')
    driver.close()
    driver.quit()

if __name__ == '__main__':
    driver = fun_login_ya()
    load_html_ya(driver)