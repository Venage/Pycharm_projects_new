import bs4
from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from openpyxl.workbook import Workbook
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')


class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36',
            'Accept-Language' : 'ru',
        }

    def load_page(self):
        #url = 'https://www.wildberries.ru/catalog/85448528/detail.aspx?target'
        url = 'https://www.wildberries.ru/catalog/zhenshchinam/odezhda/pidzhaki-i-zhakety'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text


    def pars_page(self, text:str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        #container = soup.select('div.details-section__inner-wrap')
        container = soup.select('div.product-card.j-card-item.j-good-for-listing-event')
        #self.pars_block(container=container)
        for block in container:
            self.pars_block(block=block)

        print(soup)

    def pars_block(self, container):
        logger.info(container)

    def run(self):
        text = self.load_page()
        self.pars_page(text=text)

if __name__ == '__main__':
    parser = Client()
    parser.run()


