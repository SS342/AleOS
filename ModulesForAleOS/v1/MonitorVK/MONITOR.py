from requests_html import HTMLSession
import time
from rich.console import Console
from rich.syntax import Syntax
import logging
from rich.logging import RichHandler
import sqlite3

file = str

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logging.disable(level=logging.DEBUG)
log_rich = logging.getLogger("rich")

class Monitor:
    def __init__(self, users : file, vk_api_link : str, access_token : str, v : str, connection : sqlite3.Connection, cursor : sqlite3.Cursor, tableName : str):

        self.clients : list = [line.rstrip().split("|")[0] for line in open(users, 'r')]
        self.vk_api_link = vk_api_link
        self.access_token = access_token
        self.v = v
        self.sex = [["была в сети", "был в сети"], ["в сети", "в сети"]]
        self.device = ["с мобильного", "с iPhone", "с iPad", "с Android", "с Windows Phone", "с Windows 10", "с ПК", "с VK Mobile"]
        print(self.clients)
        while True:
            for client in self.clients:
                try:
                    self.check(client)
                except Exception as e: print(str(e))

            time.sleep(10)

    def check(self, id):
        get_link = self.vk_api_link + "users.get?user_ids=" + str(id) + "&fields=sex,online,last_seen&access_token=" + self.access_token + "&v=" + self.v + "&lang=ru"
        ms = int(round(time.time() * 1000))
        content = HTMLSession().get(get_link)
        json = content.json()
        countMillis = int(round(time.time() * 1000)) - ms
        userinfo = json["response"][0]
        userstat = userinfo["last_seen"]
        nameofuser = userinfo["first_name"] + " " + userinfo["last_name"]
        ms_time = time.gmtime(int(userstat["time"]) + 10800)
        userstat = {
            "name"   : nameofuser,
            "sex"    : self.sex[int(userinfo["online"])][int(userinfo["sex"]) - 1],
            'device' : self.device[int(userstat["platform"])-1],
            'time'   : time.strftime("%d %b %Y %H:%M:%S", ms_time),
            'status' : 'online' if int(userinfo["online"]) else 'offline'
        }
        print(userstat)
        
