import requests
import json
import pymorphy2

def find_code_and_name(words, all_products):
    correct_products = []
    for product in all_products:
        product_name = product[6]
        for keyword in words:
            if keyword.lower() in product_name.lower():
                correct_products.append(product)
    return correct_products

def count_dots(item):
    return item.count('.')


def make_words(search_keyword):
    morph = pymorphy2.MorphAnalyzer()
    singular_word = morph.parse(search_keyword)[0]
    singular_word = singular_word.normal_form

    print(singular_word)

    url = "https://ws3.morpher.ru/russian/declension"
    headers = {'User-Agent': 'My Python script'}
    params = dict(
        s=singular_word,
        format="json",
    )
    arr = []
    response = requests.get(url=url, params=params, headers=headers)
    data = json.loads(response.text)
    arr.append(search_keyword)
    arr.append(data.get('Р'))
    arr.append(data.get('Д'))
    arr.append(data.get('В'))
    arr.append(data.get('Т'))
    arr.append(data.get('П'))
    if 'множественное' in data:
        arr.append(data['множественное'].get('И'))
        arr.append(data['множественное'].get('Р'))
        arr.append(data['множественное'].get('Д'))
        arr.append(data['множественное'].get('В'))
        arr.append(data['множественное'].get('Т'))
        arr.append(data['множественное'].get('П'))
    return arr