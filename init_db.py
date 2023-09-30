import sqlite3

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

# Создаем таблицу stuf
cursor.execute('''
CREATE TABLE IF NOT EXISTS stuf (
id INTEGER PRIMARY KEY,
id_subcategory INTEGER,
id_category INTEGER,    
id_sort INTEGER,
id_subgroup INTEGER,
id_bdgroup INTEGER,
inn TEXT NOT NULL,
ogrn TEXT NOT NULL,
stuf_reference TEXT NOT NULL
)
''')

# Создаем таблицу provider
cursor.execute('''
CREATE TABLE IF NOT EXISTS provider (
id INTEGER PRIMARY KEY,
inn TEXT NOT NULL,
ogrn TEXT NOT NULL,
provider_name TEXT NOT NULL
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
            cursor.execute('INSERT INTO subcategory VALUES (?, ?, ?, ?)', (id, id_prev[0], kod, name))

connection.commit()
connection.close()