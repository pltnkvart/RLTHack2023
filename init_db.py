import sqlite3
from parserWB import *

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
stuf_reference TEXT
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
#            if cursor.execute('SELECT id FROM bdgroup WHERE kod = ?', (kod,)).fetchone()[0] == None:
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
#            if cursor.execute('SELECT id FROM subgroup WHERE kod = ?', (kod,)).fetchone() == None:
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
            #if cursor.execute('SELECT id FROM sort WHERE kod = ?', (kod,)).fetchone() == None:
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
            #if cursor.execute('SELECT id FROM category WHERE kod = ?', (kod,)).fetchone() == None:
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
            #if cursor.execute('SELECT id FROM subcategory WHERE kod = ?', (kod,)).fetchone() == None:
            cursor.execute('INSERT INTO subcategory VALUES (?, ?, ?, ?)', (id, id_prev[0], kod, name))


if __name__ == '__main__':
    categories = cursor.execute('SELECT id, id_prev, name FROM subcategory')
    for category in categories.fetchall():
        products = get_products_from_wb(category[2])
        for product in products:
            id = cursor.execute('SELECT MAX(id) FROM products').fetchone()[0]
            if id == None:
                id = 0
            else:
                id += 1
            product_name = product.get('name') 
            provider = product.get('brand') 
            price = product.get('priceU')
            inn = product.get('inn')
            ogrn = product.get('ogrnip')
            id_subcategory = category[0]
            prev = cursor.execute('SELECT id, id_prev FROM category WHERE id = ?', (category[1],)).fetchone()
            id_category = prev[0]
            prev = cursor.execute('SELECT id, id_prev FROM sort WHERE id = ?', (prev[1],)).fetchone()
            id_sort = prev[0]
            prev = cursor.execute('SELECT id, id_prev FROM subgroup WHERE id = ?', (prev[1],)).fetchone()
            id_subgroup = prev[0]
            id_bdgroup = prev[1]


            print(id, id_subcategory, id_category, id_sort, id_subgroup, id_bdgroup, product_name, provider, price, inn, ogrn)


            #if cursor.execute('SELECT id FROM products WHERE (inn = ? OR ogrn = ?) AND name = ?', (inn,), (ogrn,), (name,),).fetchone() == None:
            cursor.execute('''INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (id, id_subcategory, id_category, id_sort, id_subgroup, id_bdgroup, product_name, inn, ogrn, "1234567890"))




connection.commit()
connection.close()