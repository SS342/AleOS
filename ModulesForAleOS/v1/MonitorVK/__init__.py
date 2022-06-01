file = str
import sqlite3

def startVKmonitor(users : file, connection : sqlite3.Connection, cursor : sqlite3.Cursor, tableName : str, vk_api_link : str, access_token : str, v : str):
    from MonitorVK import MONITOR
    MONITOR.Monitor(users = users, connection = connection, cursor = cursor, tableName = tableName, vk_api_link = vk_api_link, access_token = access_token, v = v)