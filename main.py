from flask import Flask
import os
from flask import render_template, url_for, request, redirect, flash
import smtplib
import sqlite3

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

@app.route('/')
def index():
    startups = db.session.query(Startup).order_by(Startup.id.desc()).all()
    if current_user.is_authenticated:
        return render_template('index.html', data = startups, user_authenticated = 1, user_id = current_user.id)
    else:
        return render_template('index.html', data = startups, user_authenticated = 0)