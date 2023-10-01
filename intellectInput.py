import requests
import json

url = "https://ws3.morpher.ru/russian/declension"

headers = {'User-Agent': 'My Python script'}

search_keyword = input("Введите ключевое слово: ")

params = dict(
    s = search_keyword,
    format ="json",
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

with open('output.txt', 'r') as file:
    lines = file.readlines()

code_to_name = {}

for line in lines:
    parts = line.split(' hui ')
    if len(parts) == 2:
        code, name = parts
        code_to_name[code] = name


def find_code_and_name(arr):
    results = []
    for code, name in code_to_name.items():
        for keyword in arr:
            if keyword.lower() in name.lower():
                results.append((code, name))
    return results


results = find_code_and_name(arr)

if results:
    print("Найдены совпадения:")
    for code, name in results:
        print(f"{code} - {name}")
else:
    print("Совпадений не найдено.")



