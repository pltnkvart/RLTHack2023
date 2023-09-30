from urllib import parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import json
import time

headers = {
    'Accept': '*/*',
    'User-Agent': 'Safari/605.1.15'
}


def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def get_firefox_options():
    options = FirefoxOptions()
    options.set_preference('devtools.jsonview.enabled', False)
    return options


def get_url_content(url: str) -> str:
    dr = webdriver.Firefox(get_firefox_options())
    dr.get(url)
    time.sleep(1)
    content = dr.page_source
    dr.quit()
    return content


def get_products_from_category(category: str) -> list[list[str]]:
    url = f'https://www.ozon.ru/search/?text={parse.quote(category)}'
    content = get_url_content(url=url)
    bs = BeautifulSoup(content, 'html.parser')
    hrefs = unique([str(link.get('href')) for link in bs.find_all('a') if '/product/' in str(link.get('href'))])
    return [[
        f'https://www.ozon.ru{parse.quote(href)}',
        f'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url={parse.quote(href)}' +
        '%26layout_container%3DpdpPage2column%26layout_page_index%3D2%26sh%3D5dWbep80WA'
    ] for href in hrefs]


def get_product_info(url: list[str]):
    content = get_url_content(url=url[0])
    bs = BeautifulSoup(content, 'html.parser')
    product = json.loads(bs.find('script', type='application/ld+json').text)
    content = get_url_content(url=url[1])
    seller = content[
             content.find('[', content.find('credentials')) + 3:
             content.find(']', content.find('credentials')) + 1
             ].split('\\",\\"')  # 0 - seller, 1 - inn
    return {
        'brand': seller[0],
        'name': product['name'],
        'id': product['offers']['url'].split('-')[-1][:-1],
        'price': product['offers']['price'],
        'rating': product['aggregateRating']['ratingValue'],
        'inn': seller[1],
    }


def get_products_from_ozon(category: str):
    links = get_products_from_category(category=category)
    products = []
    for link in links:
        products.append(get_product_info(url=link))
    return products
