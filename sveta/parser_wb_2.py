import os
import requests
from bs4 import BeautifulSoup


def infotovar(url):
    api = requests.get(url)
    result = api.content
    soup = BeautifulSoup(result, 'html.parser')
    price = soup.find('div',{'class': 'product-page__header-wrap'})#.get_text(strip=True)
    print(soup)
    #os.replace(pathtofile, 'C:\') # перемещение файла в папку

def main():
    infotovar('https://www.wildberries.ru/catalog/72833527/detail.aspx?targetUrl=GP')

if __name__ == "__main__":
    main()