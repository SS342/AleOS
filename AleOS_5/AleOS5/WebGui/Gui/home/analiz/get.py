import sqlite3
from dateutil.parser import parse
def all_time(name):
    connection = sqlite3.connect(r'C:\Users\alex2\Desktop\_ALEOS_\AleOS5\AleOS\databases\VK\users.db')
    sql = f"SELECT time FROM users WHERE name='{name}'"
    return connection.cursor().execute(sql).fetchall()