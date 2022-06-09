import sqlite3
import Gui.home.analiz as analiz
from flask import Blueprint, render_template

home_routers = Blueprint('home_routers', __name__, template_folder='templates', static_folder='static')


@home_routers.route('/')
@home_routers.route('/home')
def home():
    return render_template('home.html')


@home_routers.route('/users')
def all_users():
    conn = sqlite3.connect(r'C:\Users\alex2\Desktop\_ALEOS_\AleOS5\AleOS\databases\VK\users.db')
    cursor = conn.cursor()

    sql = "SELECT * FROM users"
    users = []
    for row in cursor.execute(sql).fetchall():
        users.append(row[0])

    return render_template('users.html', users=list(set(users)))


@home_routers.route('/users/<name>')
def get_user(name):
    return str(analiz.analiz(name))
