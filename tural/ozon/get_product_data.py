import json
import glob
import re

import pandas as pd

from lib.csv_handler import CsvHandler
global filename
filename = r'C:\PyProjects\poject_1\tural\ozon\ozon_дом_и_сад_фоторамки.xlsx'


def get_products() -> list:
    return glob.glob('products/*.html')

def get_json(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
        return json.loads(data)

def parse_data(data: dict) -> dict:
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


def main():

    products = get_products()

    df_all = pd.DataFrame(columns=['title', 'price', 'discount_price', 'brand', 'category', 'sku', 'url', 'url_pic'])
    i = 0
    for product in products:

        try:
            product_json = get_json(product)
            result = parse_data(product_json)
            df_all.loc[i] =list(result.values())

        except Exception as e:
            print(e)
        i+=1

        """
        try:
            print(product)
            product_json = get_json(product)
            result = parse_data(product_json)
            CsvHandler(result_filename).write_to_csv_semicolon(result)
        except Exception as e:
            print(e)
        """
    print(products)
    print(df_all)
    df_all.to_excel(filename, index=False)
if __name__ == '__main__':
    main()