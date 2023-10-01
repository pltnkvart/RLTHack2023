import requests
import json

def find_code_and_name(words, all_products):
    correct_products = []
    for product in all_products:
        product_name = product[6]
        for keyword in words:
            if keyword.lower() in product_name.lower():
                correct_products.append(product)
    return correct_products
'''    with open('output.txt', 'r', encoding="utf8") as file:
        lines = file.readlines()
    code_to_name = {}
    for line in lines:
        parts = line.split(' hui ')
        if len(parts) == 2:
            code, name = parts
            code_to_name[code] = name
    results = []
    added_codes = set()
    for code, name in code_to_name.items():
        for keyword in arr:
            if keyword.lower() in name.lower() and code not in added_codes:
                results.append((code, name))
                added_codes.add(code)
    return results'''

def count_dots(item):
    return item.count('.')


def find_categories(search_keyword):
    url = "https://ws3.morpher.ru/russian/declension"
    headers = {'User-Agent': 'My Python script'}
    params = dict(
        s=search_keyword,
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
    print(arr)
    return arr
    '''results = find_code_and_name(arr)
    arrCodes = []
    if results:
        print("Найдены совпадения:")
        for code, name in results:
            print(f"{code} - {name}")
            arrCodes.append(code)
    else:
        print("Совпадений не найдено.")
    arrCodes = sorted(arrCodes, key=count_dots, reverse=True)
    return arrCodes'''


'''if __name__ == "__main__":
    find_categories('труба')'''