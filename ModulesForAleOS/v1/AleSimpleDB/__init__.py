import sqlite3

def Connect(path="database.db"):
    from AleSimpleDB import connect
    return connect.Connect(path).return_conn_cur()


def types():
    from AleSimpleDB import data_types
    return data_types.Types()


def create_table(connection : sqlite3.Connection, cursor : sqlite3.Cursor, data : dict):
    from AleSimpleDB.create_table import create
    create(data=data, connection=connection, cursor=cursor)


def get_all_writes(cursor : sqlite3.Cursor, tableName : str) -> list:
    from AleSimpleDB.get import get_all_writes as _get_all_writes
    return _get_all_writes(cursor, tableName)


def get_writes_by(cursor : sqlite3.Cursor, tableName : str, param: str, query : str):
    from AleSimpleDB.get import get_writes_by as _get_writes_by
    return _get_writes_by(cursor, tableName, param, query)


def get_last(cursor : sqlite3.Cursor, tableName : str):
    from AleSimpleDB.get import get_last as _get_last
    return _get_last(cursor, tableName)

def new_write(connection : sqlite3.Connection, cursor : sqlite3.Cursor, tableName : str, data : list):
    from AleSimpleDB.write import new_write as _new_write
    msg = _new_write(connection, cursor, tableName, data)
    if msg: return msg

def get_last_by(cursor : sqlite3.Cursor, tableName : str, param: str, query : str):
    from AleSimpleDB.get import get_last_by as _get_last_by
    return _get_last_by(cursor, tableName, param, query)

def comparison(cursor : sqlite3.Cursor, tableName : str, param: str, query : str, compar : str, param_num : int):
    from AleSimpleDB.get import comparison as _comparison
    return _comparison(cursor, tableName, param, query, compar, param_num)