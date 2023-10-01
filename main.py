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
        products = query_db('SELECT * FROM products ORDER BY rating DESC')
        for word in search.split(' '): 
            words = make_words(word)
            products = find_code_and_name(words, products)
        index = 1
        for i in range(len(products)):
            find_providers = query_db('SELECT * FROM provider WHERE inn = ? or ogrn = ?', (products[i][7], products[i][8]))
            find_kod = query_db('SELECT * FROM subcategory WHERE id = ?', (products[i][1],))
            for provider in find_providers:
                products[i] = products[i] + (provider[3],)
            for kod in find_kod:
                products[i] = products[i] + (kod[2],)
            products[i] = products[i] + (index,)
            index += 1
        return render_template('index.html', products = products)
    else:
        return render_template('index.html', products = products)

if __name__ == "__main__":
    app.run()

connection.commit()
connection.close()