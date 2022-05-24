
# -*- coding: utf-8 -*-

from requests_html import HTMLSession
import time
import sqlite3
from rich.console import Console
from rich.syntax import Syntax
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logging.disable(level=logging.DEBUG)
log_rich = logging.getLogger("rich")

Error001 : str = "Error001" # db list out of range
Error002 : str = "Error002" #

console = Console()
vk_api_link = "https://api.vk.com/method/"
access_token = "2cbc788c2cbc788c2cbc788c082cde2a0322cbc2cbc788c7670e35f9811d37cde017f2b"
v = "5.85"

log_rich.info(f"[ AleOS-vk ] : VK API link: {vk_api_link}")
log_rich.info(f"[ AleOS-vk ] : Access token: {access_token}")
log_rich.info(f"[ AleOS-vk ] : version : {v}")

log_rich.info(f"[ AleOS-vk ] : Извлечение пользовательских id")
path = "UserNetworkMonitoring\\VK\\usr.txt"
with open(path, "r") as usr:
    users = [line.rstrip() for line in usr]
num_of_user = len(users)

db = None

def log(stats):
    
    text = f"[ AleOS-vk ] : {stats['name']} {'В сети' if stats['status'] == 'online' else 'Не в сети'} {stats['device'] if stats['status'] == 'online' else ''} {stats['time']}"
    console.log(text, log_locals=False)

class DataBase(object):
    def __init__(self):
        self.connection = sqlite3.connect("UserNetworkMonitoring\\VK\\users.db" if __name__ == '__main__' else "users.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        sql = """CREATE TABLE IF NOT EXISTS users(
                    name STRING,
                    device STRING,
                    status STRING,
                    time STRING);
                """
        self.cursor.execute(sql)
        self.connection.commit()

    def getLastOnline(self, name, status):

        try: return True if status == self.cursor.execute(f"SELECT status FROM users WHERE name = '{name}'").fetchall()[-1][0] else False
        except: log_rich.error(Error001); return Error001

    def writeInfo(self, stats):
        data = self.getLastOnline(stats['name'], stats['status'])
        if not(data):
            self.updateUser(stats)
            log(stats)
        elif (data) == Error001:
            self.updateUser(stats)
            log(stats)
        
        elif data: pass
        else: log_rich.error(Error002)

    def updateUser(self, stats):
        sql = f"INSERT INTO users values('{stats['name']}', '{stats['device']}', '{stats['status']}', '{stats['time']}')"
        self.cursor.execute(sql)
        self.connection.commit()


def check_user(ids):

    db = DataBase()
    db.create_table()

    user_ids = ",".join(str(e) for e in ids)
    get_link = vk_api_link + "users.get?user_ids=" + str(user_ids) + "&fields=sex,online,last_seen&access_token=" + access_token + "&v=" + v + "&lang=ru"

    ms = int(round(time.time() * 1000))
    content = HTMLSession().get(get_link)
    json = content.json()
    countMillis = int(round(time.time() * 1000)) - ms

    sex = [["была в сети", "был в сети"], ["в сети", "в сети"]]
    device = ["с мобильного", "с iPhone", "с iPad", "с Android", "с Windows Phone", "с Windows 10", "с ПК", "с VK Mobile"]

    for i in range(num_of_user):
        userinfo = json["response"][i]
        userstat = userinfo["last_seen"]

        nameofuser = userinfo["first_name"] + " " + userinfo["last_name"]
        ms_time = time.gmtime(int(userstat["time"]) + 10800)

        userstat = {
            "name"   : nameofuser,
            "sex"    : sex[int(userinfo["online"])][int(userinfo["sex"]) - 1],
            'device' : device[int(userstat["platform"])-1],
            'time'   : time.strftime("%d %b %Y %H:%M:%S", ms_time),
            'status' : 'online' if int(userinfo["online"]) else 'offline'
        }
        
        db.writeInfo(userstat)


def run():
    log_rich.info(f"[ AleOS-vk ] : Подключение к базе данных")
    db = DataBase()
    db.create_table()
    log_rich.info(f"[ AleOS-vk ] : Подключение установленно")
    runtimes = 0

    users.sort()
    timer_delay = 0.1
    log_rich.info(f"[ AleOS-vk ] : Задержка цикла = {60 * float(timer_delay)} c")

    while True:
        runtimes += 1

        try:  
            if users is None and users == "": break
            else: check_user(users)
        except Exception as e: print(str(e))
            
        time.sleep(60 * float(timer_delay))
run()

