import sqlite3

def get_all_writes(cursor : sqlite3.Cursor, tableName : str):
    return cursor.execute(f"SELECT * FROM {tableName}").fetchall()


def get_writes_by(cursor : sqlite3.Cursor, tableName : str, param: str, query : str): 
    return cursor.execute(f"SELECT * FROM {tableName} WHERE {param} = '{query}'").fetchall()


def get_last(cursor : sqlite3.Cursor, tableName : str):
    return cursor.execute(f'SELECT * FROM {tableName}').fetchall()[-1]

def get_last_by(cursor : sqlite3.Cursor, tableName : str, param: str, query : str):
    return cursor.execute(f'SELECT * FROM {tableName} WHERE {param} = "{query}"').fetchall()[-1]

def comparison(cursor : sqlite3.Cursor, tableName : str, param: str, query : str, compar : str, param_num : int):
    return str(cursor.execute(f'SELECT * FROM {tableName} WHERE {param} = "{query}"').fetchall()[-1][param_num]) == compar