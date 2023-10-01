from flask import Flask
import os
from flask import render_template, url_for, request, redirect, flash
import smtplib
import sqlite3

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        search = request.form['search']
        products = 
        return render_template('index.html', products)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run()

connection.commit()
connection.close()