import sqlite3
from parserWB import *
from parserOZON import *

# Создаем подключение к базе данных (файл my_database.db будет создан)
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()


# Создаем таблицу bdgroup
cursor.execute("""
CREATE TABLE IF NOT EXISTS bdgroup (
id INTEGER PRIMARY KEY,
kod TEXT NOT NULL,
name TEXT NOT NULL
)
""")

# Создаем таблицу subgroup
cursor.execute('''
CREATE TABLE IF NOT EXISTS subgroup (
id INTEGER PRIMARY KEY,
id_prev INTEGER,
kod TEXT NOT NULL,
name TEXT NOT NULL
)
''')

# Создаем таблицу sort
cursor.execute('''
CREATE TABLE IF NOT EXISTS sort (
id INTEGER PRIMARY KEY,
id_prev INTEGER,
kod TEXT NOT NULL,
name TEXT NOT NULL
)
''')

# Создаем таблицу category
cursor.execute('''
CREATE TABLE IF NOT EXISTS category (
id INTEGER PRIMARY KEY,
id_prev INTEGER,
kod TEXT NOT NULL,
name TEXT NOT NULL
)
''')

# Создаем таблицу subcategory
cursor.execute('''
CREATE TABLE IF NOT EXISTS subcategory (
id INTEGER PRIMARY KEY,
id_prev INTEGER,
kod TEXT NOT NULL,
name TEXT NOT NULL
)
''')

# Создаем таблицу products
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
id INTEGER PRIMARY KEY,
id_subcategory INTEGER,
id_category INTEGER,    
id_sort INTEGER,
id_subgroup INTEGER,
id_bdgroup INTEGER,
name TEXT,
inn TEXT,
ogrn TEXT,
price FLOAT,
rating FLOAT,
product_reference TEXT
)
''')

# Создаем таблицу provider
cursor.execute('''
CREATE TABLE IF NOT EXISTS provider (
id INTEGER PRIMARY KEY,
inn TEXT,
ogrn TEXT,
provider_name TEXT
)
''')


with open('ОКПД2.txt', 'r', encoding="utf8") as f:
    while True:
        line = f.readline()
        if not line:
            break
        kod = line[:line.find(',')]
        name = line[(line.find(',') + 2):]
        lenght = len(kod)

        if lenght == 5:
            id = cursor.execute('SELECT MAX(id) FROM bdgroup').fetchone()[0]
            if id == None:
                id = 0
            else:
                id += 1
            if cursor.execute('SELECT COUNT(1) FROM bdgroup WHERE kod = ?', (kod,)).fetchone()[0] == 0:
                cursor.execute('INSERT INTO bdgroup VALUES (?, ?, ?)', (id, kod, name))

        elif lenght == 7:  
            id = cursor.execute('SELECT MAX(id) FROM subgroup').fetchone()[0]
            if id == None:
                id = 0
            else:
                id += 1
            prev_kod = kod[:5]
            cursor.execute('SELECT id FROM bdgroup WHERE kod = ?', (prev_kod,))
            id_prev = cursor.fetchone()
            if id_prev == None:
                id_prev = [-1]
            if cursor.execute('SELECT COUNT(1) FROM subgroup WHERE kod = ?', (kod,)).fetchone()[0] == 0:
                cursor.execute('INSERT INTO subgroup VALUES (?, ?, ?, ?)', (id, id_prev[0], kod, name))

        elif lenght == 8:
            id = cursor.execute('SELECT MAX(id) FROM sort').fetchone()[0]
            if id == None:
                id = 0
            else:
                id += 1
            prev_kod = kod[:7]
            cursor.execute('SELECT id FROM subgroup WHERE kod = ?', (prev_kod,))
            id_prev = cursor.fetchone()
            if id_prev == None:
                id_prev = [-1]
            if cursor.execute('SELECT COUNT(1) FROM sort WHERE kod = ?', (kod,)).fetchone()[0] == 0:
                cursor.execute('INSERT INTO sort VALUES (?, ?, ?, ?)', (id, id_prev[0], kod, name))
        
        elif (lenght == 12 and kod[-1] == "0"):
            id = cursor.execute('SELECT MAX(id) FROM category').fetchone()[0]
            if id == None:
                id = 0
            else:
                id += 1
            prev_kod = kod[:8]
            cursor.execute('SELECT id FROM sort WHERE kod = ?', (prev_kod,))
            id_prev = cursor.fetchone()
            if id_prev == None:
                id_prev = [-1]
            if cursor.execute('SELECT COUNT(1) FROM category WHERE kod = ?', (kod,)).fetchone()[0] == 0:
                cursor.execute('INSERT INTO category VALUES (?, ?, ?, ?)', (id, id_prev[0], kod, name))

        else:
            id = cursor.execute('SELECT MAX(id) FROM subcategory').fetchone()[0]
            if id == None:
                id = 0
            else:
                id += 1
            prev_kod = kod[:-1] + "0"
            cursor.execute('SELECT id FROM category WHERE kod = ?', (prev_kod,))
            id_prev = cursor.fetchone()
            if id_prev == None:
                id_prev = [-1]
            if cursor.execute('SELECT COUNT(1) FROM subcategory WHERE kod = ?', (kod,)).fetchone()[0] == 0:
                cursor.execute('INSERT INTO subcategory VALUES (?, ?, ?, ?)', (id, id_prev[0], kod, name))
                
connection.commit()

def pars_wb(categories):
    for category in categories:
        products = get_products_from_wb(category[2])
        for product in products:
            id = cursor.execute('SELECT MAX(id) FROM products').fetchone()[0]
            if id == None:
                id = 0
            else:
                id += 1
            product_name = product.get('name') 
            provider = product.get('brand') 
            price = product.get('price')
            inn = product.get('inn')
            ogrn = product.get('ogrnip')
            rating = product.get('rating')
            product_reference = "https://www.wildberries.ru/catalog/" + str(product.get('id')) + "/detail.aspx"
            id_subcategory = category[0]
            prev = cursor.execute('SELECT id, id_prev FROM category WHERE id = ?', (category[1],)).fetchone()
            id_category = prev[0]
            prev = cursor.execute('SELECT id, id_prev FROM sort WHERE id = ?', (prev[1],)).fetchone()
            id_sort = prev[0]
            prev = cursor.execute('SELECT id, id_prev FROM subgroup WHERE id = ?', (prev[1],)).fetchone()
            id_subgroup = prev[0]
            id_bdgroup = prev[1]
            flag = cursor.execute('SELECT COUNT(1) FROM products WHERE (inn = ? OR ogrn = ?) AND name = ?', (inn, ogrn, product_name)).fetchone()[0]
            if len(inn) != 0 or len(ogrn) != 0:
                if flag == 0:
                    cursor.execute('''INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (id, id_subcategory, id_category, id_sort, id_subgroup, id_bdgroup, product_name, inn, ogrn, price, rating, product_reference))
                else:
                    obj = cursor.execute('SELECT inn, ogrn, price, rating FROM products WHERE (inn = ? OR ogrn = ?) AND name = ?', (inn, ogrn, product_name)).fetchone()
                    if(obj == None):
                        cursor.execute('UPDATE products SET inn = ? WHERE ogrn = ? AND name = ?', (inn, ogrn, product_name))
                    elif len(obj[0]) == 0:
                        cursor.execute('UPDATE products SET inn = ? WHERE ogrn = ? AND name = ?', (inn, ogrn, product_name))
                    if(obj == None):
                        cursor.execute('UPDATE products SET ogrn = ? WHERE inn = ? AND name = ?', (ogrn, inn, product_name))
                    elif len(obj[1]) == 0:
                        cursor.execute('UPDATE products SET ogrn = ? WHERE inn = ? AND name = ?', (ogrn, inn, product_name))
                    if(price < obj[2]):
                        cursor.execute('UPDATE products SET price = ?, product_reference = ? WHERE (inn = ? OR ogrn = ?) AND name = ?', (price, product_reference, inn, ogrn, product_name))
                    rating = (rating + obj[3]) / 2
                    cursor.execute('UPDATE products SET rating = ? WHERE (inn = ? OR ogrn = ?) AND name = ?', (rating, inn, ogrn, product_name))

                if cursor.execute('SELECT COUNT(1) FROM provider WHERE inn = ? OR ogrn = ?', (inn, ogrn)).fetchone()[0] == 0:
                    id = cursor.execute('SELECT MAX(id) FROM provider').fetchone()[0]
                    if id == None:
                        id = 0
                    else:
                        id += 1
                    cursor.execute('''INSERT INTO provider VALUES (?, ?, ?, ?)''', (id, inn, ogrn, provider))
                else:
                    obj = cursor.execute('SELECT inn, ogrn FROM provider WHERE (inn = ? OR ogrn = ?) AND provider_name = ?', (inn, ogrn, provider)).fetchone()
                    if obj == None:
                        cursor.execute('UPDATE provider SET inn = ? WHERE ogrn = ? AND provider_name = ?', (inn, ogrn, provider))
                    elif len(obj[0]) == 0:
                        cursor.execute('UPDATE provider SET inn = ? WHERE ogrn = ? AND provider_name = ?', (inn, ogrn, provider))
                    if obj == None:
                        cursor.execute('UPDATE provider SET ogrn = ? WHERE inn = ? AND provider_name = ?', (ogrn, inn, provider))
                    elif len(obj[1]) == 0:
                        cursor.execute('UPDATE provider SET ogrn = ? WHERE inn = ? AND provider_name = ?', (ogrn, inn, provider))
        connection.commit()

def pars_ozon(categories):
    for category in categories:
        products = get_products_from_wb(category[2])
        for product in products:
            id = cursor.execute('SELECT MAX(id) FROM products').fetchone()[0]
            if id == None:
                id = 0
            else:
                id += 1
            product_name = product.get('name') 
            provider = product.get('brand') 
            price = product.get('price')
            inn = product.get('inn')
            ogrn = product.get('ogrnip')
            rating = product.get('rating')
            product_reference = "https://www.ozon.ru/product/" + str(product.get('id'))
            id_subcategory = category[0]
            prev = cursor.execute('SELECT id, id_prev FROM category WHERE id = ?', (category[1],)).fetchone()
            id_category = prev[0]
            prev = cursor.execute('SELECT id, id_prev FROM sort WHERE id = ?', (prev[1],)).fetchone()
            id_sort = prev[0]
            prev = cursor.execute('SELECT id, id_prev FROM subgroup WHERE id = ?', (prev[1],)).fetchone()
            id_subgroup = prev[0]
            id_bdgroup = prev[1]
            flag = cursor.execute('SELECT COUNT(1) FROM products WHERE (inn = ? OR ogrn = ?) AND name = ?', (inn, ogrn, product_name)).fetchone()[0]
            if len(inn) != 0 or len(ogrn) != 0:
                if flag == 0:
                    cursor.execute('''INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (id, id_subcategory, id_category, id_sort, id_subgroup, id_bdgroup, product_name, inn, ogrn, price, rating, product_reference))
                else:
                    obj = cursor.execute('SELECT inn, ogrn, price, rating FROM products WHERE (inn = ? OR ogrn = ?) AND name = ?', (inn, ogrn, product_name)).fetchone()
                    if(obj == None):
                        cursor.execute('UPDATE products SET inn = ? WHERE ogrn = ? AND name = ?', (inn, ogrn, product_name))
                    elif len(obj[0]) == 0:
                        cursor.execute('UPDATE products SET inn = ? WHERE ogrn = ? AND name = ?', (inn, ogrn, product_name))
                    if(obj == None):
                        cursor.execute('UPDATE products SET ogrn = ? WHERE inn = ? AND name = ?', (ogrn, inn, product_name))
                    elif len(obj[1]) == 0:
                        cursor.execute('UPDATE products SET ogrn = ? WHERE inn = ? AND name = ?', (ogrn, inn, product_name))
                    if(price < obj[2]):
                        cursor.execute('UPDATE products SET price = ?, product_reference = ? WHERE (inn = ? OR ogrn = ?) AND name = ?', (price, product_reference, inn, ogrn, product_name))
                    rating = (rating + obj[3]) / 2
                    cursor.execute('UPDATE products SET rating = ? WHERE (inn = ? OR ogrn = ?) AND name = ?', (rating, inn, ogrn, product_name))

                if cursor.execute('SELECT COUNT(1) FROM provider WHERE inn = ? OR ogrn = ?', (inn, ogrn)).fetchone()[0] == 0:
                    id = cursor.execute('SELECT MAX(id) FROM provider').fetchone()[0]
                    if id == None:
                        id = 0
                    else:
                        id += 1
                    cursor.execute('''INSERT INTO provider VALUES (?, ?, ?, ?)''', (id, inn, ogrn, provider))
                else:
                    obj = cursor.execute('SELECT inn, ogrn FROM provider WHERE (inn = ? OR ogrn = ?) AND provider_name = ?', (inn, ogrn, provider)).fetchone()
                    if obj == None:
                        cursor.execute('UPDATE provider SET inn = ? WHERE ogrn = ? AND provider_name = ?', (inn, ogrn, provider))
                    elif len(obj[0]) == 0:
                        cursor.execute('UPDATE provider SET inn = ? WHERE ogrn = ? AND provider_name = ?', (inn, ogrn, provider))
                    if obj == None:
                        cursor.execute('UPDATE provider SET ogrn = ? WHERE inn = ? AND provider_name = ?', (ogrn, inn, provider))
                    elif len(obj[1]) == 0:
                        cursor.execute('UPDATE provider SET ogrn = ? WHERE inn = ? AND provider_name = ?', (ogrn, inn, provider))
        connection.commit()

if __name__ == '__main__':
    categories = cursor.execute('SELECT id, id_prev, name FROM subcategory').fetchall()
    pars_wb(categories)
    pars_ozon(categories)


connection.commit()
connection.close()