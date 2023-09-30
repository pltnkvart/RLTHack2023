import requests
import pandas as pd
from urllib import parse
import json

def get_all_products_in_search_result(category: str):
    for page in range(1, 101):
        url = (f"https://search.wb.ru/exactmatch/ru/common/v4/search?"
               f"appType=1&curr=rub"
               f"&dest=-1029256,-102269,-2162196,-1257786"
               f"&page={page}&pricemarginCoeff=1.0"
               f"&query={parse.quote(category)}&reg=0"
               f"&resultset=catalog&sort=popular&spp=0")
        return url


def get_category(category: str):
    url = get_all_products_in_search_result(category)

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.by',
        'Referer': 'https://www.wildberries.by/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': 'Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
    }

    while True:
        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except json.decoder.JSONDecodeError:
            continue


def find_basket(_short_id):
    if 0 <= _short_id <= 143:
        basket = '01'
    elif 144 <= _short_id <= 287:
        basket = '02'
    elif 288 <= _short_id <= 431:
        basket = '03'
    elif 432 <= _short_id <= 719:
        basket = '04'
    elif 720 <= _short_id <= 1007:
        basket = '05'
    elif 1008 <= _short_id <= 1061:
        basket = '06'
    elif 1062 <= _short_id <= 1115:
        basket = '07'
    elif 1116 <= _short_id <= 1169:
        basket = '08'
    elif 1170 <= _short_id <= 1313:
        basket = '09'
    elif 1314 <= _short_id <= 1601:
        basket = '10'
    elif 1602 <= _short_id <= 1655:
        basket = '11'
    elif 1656 <= _short_id <= 1919:
        basket = '12'
    else:
        basket = '13'
    return basket


def prepare_items(response):
    products = []
    products_raw = response.get('data', {}).get('products', None)
    if products_raw != None and len(products_raw) > 0:
        for product in products_raw:

            products.append({
                'brand': product.get('brand', None),
                'name': product.get('name', None),
                'id': product.get('id', None),
                'sale': product.get('sale', None),
                'priceU': float(product.get('priceU', None)) / 100 if product.get('priceU', None) != None else None,
                'salePriceU': float(product.get('salePriceU', None)) / 100 if product.get('salePriceU',
                                                                                          None) != None else None,
                'url': f"https://basket-{find_basket(int(product.get('id', None)) // 100000)}.wb.ru/vol{int(product.get('id', None)) // 100000}/part{int(product.get('id', None)) // 1000}/{int(product.get('id', None))}/info/sellers.json"
            })

    return products


def main():
    category = input()
    response = get_category(category)
    products = prepare_items(response)

    pd.DataFrame(products).to_csv('products.csv', index=False)


if __name__ == '__main__':
    main()
