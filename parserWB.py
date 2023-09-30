import requests
import pandas as pd
from urllib import parse
from json.decoder import JSONDecodeError


headers = {
    'Accept': '*/*',
    'User-Agent': 'Safari/605.1.15'
}


def get_safe_json_from_url(url: str):
    while True:
        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except JSONDecodeError:
            continue


def get_all_products_in_search_result(category: str):
    products = []
    for page in range(1, 101):
        url = (f"https://search.wb.ru/exactmatch/ru/common/v4/search?"
               f"appType=1&curr=rub"
               f"&dest=-1029256,-102269,-2162196,-1257786"
               f"&page={page}&pricemarginCoeff=1.0"
               f"&query={parse.quote(category)}&reg=0"
               f"&resultset=catalog&sort=popular&spp=0")
        response = get_safe_json_from_url(url=url)
        products_curent = parse_response_to_products(response=response)
        if len(products_curent) > 0:
            products += products_curent
        else:
            break
    return products


def get_basket_id(short_id: int) -> str:
    if 0 <= short_id <= 143:
        return '01'
    elif 144 <= short_id <= 287:
        return '02'
    elif 288 <= short_id <= 431:
        return '03'
    elif 432 <= short_id <= 719:
        return '04'
    elif 720 <= short_id <= 1007:
        return '05'
    elif 1008 <= short_id <= 1061:
        return '06'
    elif 1062 <= short_id <= 1115:
        return '07'
    elif 1116 <= short_id <= 1169:
        return '08'
    elif 1170 <= short_id <= 1313:
        return '09'
    elif 1314 <= short_id <= 1601:
        return '10'
    elif 1602 <= short_id <= 1655:
        return '11'
    elif 1656 <= short_id <= 1919:
        return '12'
    return '13'


def get_seller_from_product_id(product_id: str):
    url = (f'https://basket-{get_basket_id(int(product_id[:-5]))}.wb.ru/'
           f'vol{product_id[:-5]}/part{product_id[:-3]}/{product_id}/info/sellers.json')
    return get_safe_json_from_url(url=url)


def parse_response_to_products(response):
    products_ret = []
    products_raw = response.get('data', {}).get('products', None)
    if products_raw is not None and len(products_raw) > 0:
        for product in products_raw:
            seller = get_seller_from_product_id(str(product.get('id', None)))
            products_ret.append({
                'brand': product.get('brand', ''),
                'name': product.get('name', ''),
                'id': product.get('id', ''),
                'sale': product.get('sale', ''),
                'priceU': float(product.get('priceU', 0)) / 100,
                'salePriceU': float(product.get('salePriceU', 0)) / 100,
                'inn': seller.get('inn', ''),
                'ogrnip': seller.get('ogrnip', ''),
            })
    return products_ret


def main(category: str):
    products = get_all_products_in_search_result(category=category)
    pd.DataFrame(products).to_csv('products.csv', index=False)
