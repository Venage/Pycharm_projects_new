import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

url = "https://www.wildberries.ru/catalog/72833527/detail.aspx?targetUrl=GP"
id = url.split("/")[-2]
url_price_history = f"https://wbx-content-v2.wbstatic.net/price-history/{id}.json"
current_date = "{:%d.%m.%Y}".format(datetime.now())
output_file = f"{id}.csv"


def get_title_and_current_price(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('div', {'class': 'product-page__header-wrap'})
    #.text

    print(soup)
    print(type(soup))
    #current_price = float(soup.find(class_="price-block__final-price").text.strip().replace('₽', '').replace('\xa0', ''))
    #return title, current_price

if __name__ == '__main__':
    get_title_and_current_price(url)

"""
def get_price_history(url_price_history):
    r = requests.get(url_price_history).json()

    date_row = []
    price_row = []

    for i in r:
        date = datetime.fromtimestamp(i['dt'])
        date = date.strftime('%d.%m.%Y')
        date_row.append(date)
        price_row.append(float((i['price']['RUB']) / 100))
    date_row.append(current_date)
    price_row.append(current_price)
    return date_row, price_row

def add_data_to_csv(row):
    with open(output_file, "a", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(row)


if __name__ == '__main__':
    title, current_price = get_title_and_current_price(url)
    date_row, price_row = get_price_history(url_price_history)
    header_row = [title, url]
    add_data_to_csv(header_row)
    add_data_to_csv(date_row)
    add_data_to_csv(price_row)
"""
