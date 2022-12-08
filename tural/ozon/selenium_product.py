from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import random

import lib.config

class UseSelenium:
    def __init__(self, url: str, filename: str):
        self.url = url
        self.filename = filename

    def save_page(self):
        users = [{'http_proxy': '193.31.103.210:9244',
                  'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'},
                 {'http_proxy': '193.31.101.224:9604',
                  'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'},
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

        s = Service(executable_path="C:/Users/venag/Downloads/chromedriver_win32/chromedriver.exe")

        #driver = webdriver.Chrome(options=options, service=s, seleniumwire_options=options_proxy)
        driver = webdriver.Chrome(options=options, service=s)

        try:
            driver.get(self.url)
            elem = driver.find_element(By.TAG_NAME, "pre").get_attribute('innerHTML')
            with open(r'C:\PyProjects\poject_1\tural\ozon\products/' + self.filename, 'w', encoding='utf-8') as f:
                f.write(elem)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def __get_headers_proxy(self) -> dict:
        '''
        The config file must have dict:
            {
                'http_proxy':'http://user:password@ip:port',
                'user-agent': 'user_agent name'
            }
        '''

        """
                   users = lib.config.USER_AGENTS_PROXY_LIST
                   persona = random.choice(users)
                   """
        try:
            users = [{'http_proxy': 'http://YzY8Vu:UQpB3Z@217.29.62.212:11045',
                      'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}]
            persona = random.choice(users)

        except ImportError:
            persona = None
        return persona



