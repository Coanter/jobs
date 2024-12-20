from flask import Blueprint, render_template, request
import sqlite3

main = Blueprint('main', __name__)

def get_db_connection():
    conn = sqlite3.connect('database/head_hunter.db')
    conn.row_factory = sqlite3.Row
    return conn

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/analytics', methods=['GET'])
def analytics():
    city_filter = request.args.get('city', '')
    conn = get_db_connection()
    if city_filter:
        rows = conn.execute('SELECT * FROM vacancies WHERE city = ?', (city_filter,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM vacancies').fetchall()
    conn.close()
    return render_template('analytics.html', vacancies=rows)
