from flask import Flask, g
import os
from flask import render_template, url_for, request, redirect, flash
import smtplib
import sqlite3
from intellectInput import *

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
connection = sqlite3.connect('my_database.db')
DATABASE = 'my_database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv



@app.route('/', methods = ['POST', 'GET'])
def index():
    products = []
    if request.method == 'POST':
        search = request.form['search']
        categories = find_categories(search)
        for kod in categories:
            lenght =  len(kod)
            if (lenght == 12 and kod[-1] == "0"):
                id_category = query_db('SELECT * FROM category WHERE kod = ?', [kod])
            elif (lenght == 12):
                id_category = query_db('SELECT * FROM subcategory WHERE kod = ?', [kod])

            for id in id_category:
                find_products = query_db('SELECT * FROM products WHERE id_subcategory = ? ORDER BY rating DESC', [id[0]])
                for product in find_products:
                    products.append(product)

        index = 1
        for i in range(len(products)):
            find_providers = query_db('SELECT * FROM provider WHERE inn = ? or ogrn = ?', (products[i][7], products[i][8]))
            for provider in find_providers:
                products[i] = products[i] + (provider[3],)
            products[i] = products[i] + (index,)
            index += 1
        
        return render_template('index.html', products = products)
    else:
        return render_template('index.html', products = products)


if __name__ == "__main__":
    app.run()

connection.commit()
connection.close()