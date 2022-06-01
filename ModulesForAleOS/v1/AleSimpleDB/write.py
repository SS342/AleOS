import sqlite3

def new_write(connection : sqlite3.Connection, cursor : sqlite3.Cursor, tableName : str, data : list):
    sql = f"INSERT INTO {tableName} values("
    for el in data:
        sql += f"'{el}', "
    sql = sql[:-2] + ')'
    try:
        cursor.execute(sql)
        connection.commit()
        return False
    except Exception as e: return "Error write" + str(e)