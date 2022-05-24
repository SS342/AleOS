from datetime import datetime, timedelta

from telethon import TelegramClient, events, connection
from telethon.tl.types import UserStatusRecently, UserStatusEmpty, UserStatusOnline, UserStatusOffline, PeerUser, PeerChat, PeerChannel
from time import mktime, sleep
import telethon.sync
from threading import Thread
import collections
from rich.console import Console
from rich.syntax import Syntax
import logging
from rich.logging import RichHandler
import sqlite3

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logging.disable(level=logging.DEBUG)
log_rich = logging.getLogger("rich")

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
API_HASH = 'd8a8389f6d61a3f1d9850fb08f0064e3'
API_ID = '18452904'
BOT_TOKEN = "1870153181:AAFwniEcHvluk5A20lxtmsNLtOQvuFjkY9Y"
USER_NAME = "allelleo"

v = 1.0

log_rich.info(f"[ AleOS-tg ] : API HASH: {API_HASH}")
log_rich.info(f"[ AleOS-tg ] : API ID: {API_ID}")
log_rich.info(f"[ AleOS-tg ] : BOT TOKEN: {BOT_TOKEN}")
log_rich.info(f"[ AleOS-tg ] : USER NAME: {USER_NAME}")
log_rich.info(f"[ AleOS-tg ] : version : {v}")



client = TelegramClient('data_thief', API_ID, API_HASH)
console = Console()
client.connect()
client.start()
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def log(stats):
    
    text = f"[ AleOS-tg ] : {stats['first_name']} {'В сети' if stats['status'] == 'online' else 'Не в сети'} {stats['username']} {stats['id']}"
    console.log(text, log_locals=False)

class DataBase(object):
    def __init__(self):
        self.connection = sqlite3.connect("UserNetworkMonitoring\\TG\\users.db" if __name__ == '__main__' else "users.db")
        self.cursor = self.connection.cursor()
    
    def create_table(self):
        sql = """CREATE TABLE IF NOT EXISTS users(
                    name STRING,
                    nick STRING,
                    status STRING,
                    time STRING,
                    id STRING);
                """
        self.cursor.execute(sql)
        self.connection.commit()

    def get_user_status(self, stats):
        sql = f"SELECT status FROM users WHERE id = '{stats['id']}'"
        try: data = self.cursor.execute(sql).fetchall()[-1][0]; return stats['status'] == data
        except: self.create_user(stats)

    def create_user(self, stats):
        sql = f"INSERT INTO users values('{stats['first_name']}', '{stats['username']}', '{stats['status']}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{stats['id']}')"
        self.cursor.execute(sql)
        self.connection.commit()

db = DataBase()
db.create_table()


class MyDate(object):
    def __init__(self, date):
        self.date, self.time = date.split()[0], date.split()[1]
        self.Y, self.M, self.D = int(self.date.split('-')[0]), int(self.date.split('-')[1]), int(self.date.split('-')[2])
        self.h, self.m, self.s = int(self.time.split(':')[0]), int(self.time.split(':')[1]), int(self.time.split(':')[2])

    def __gt__(self, other):
        if self.Y > other.Y:
            return False
        else:
            if self.M > other.M:
                return False
            else:
                if self.D > other.D:
                    return False
                else:
                    if self.h > other.h:
                        return False
                    else:
                        if self.m > other.m:
                            return False
                        else:
                            if self.s > other.s:
                                return False
                            else: return True

def debugPrint(msg):
    print(msg)

def mytime(UsrStats, date):
    time = date.split()[0] + " " + date.split()[1].split('+')[0]

    stats = {
        "id" :  UsrStats.id,
        'first_name' : UsrStats.first_name,
        "username" : UsrStats.username,
        'phone' : UsrStats.phone,
        'status' : 'online' if (str(datetime.now().strftime("%Y-%m-%d %H:%M")) == (str(datetime.strptime(time, "%Y-%m-%d %H:%M:%S") + timedelta(hours=3)).split()[1])[:-3]) or not((MyDate((str(datetime.strptime(time, "%Y-%m-%d %H:%M:%S") + timedelta(hours=3)))) > MyDate(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))) else "offline",
    }
    if not(db.get_user_status(stats)):
        db.create_user(stats)
        log(stats)
    

def myPrint(stats):
    if isinstance(stats.status, UserStatusOffline):
        mytime(stats, str(stats.status.was_online))
    else:
        if isinstance(stats.status, UserStatusOnline):
            mytime(stats, str(stats.status.expires))
        else:
            if isinstance(stats.status, UserStatusRecently): print({
                                                                "id" :  stats.id,
                                                                'first_name' : stats.first_name,
                                                                "username" : stats.username,
                                                                'phone' : stats.phone,
                                                                'status' : "recently",
                                                                }
                                                            ) if not(db.get_user_status(stats)) else ""

def user_update_event_handler(_id):

    try:
        user_details = client.get_entity(_id)
        
        myPrint(user_details)
    except Exception as e:
        #print(f"[{_id}] : {str(e)}")
        pass

if __name__ == "__main__":
    path = "UserNetworkMonitoring\\TG\\usr.txt"
else:
    path = "UserNetworkMonitoring\\TG\\usr.txt"
with open(path, "r") as usr:
    usersId = [int(line.rstrip()) for line in usr]
def run():
    while True:
        for _id in usersId:
            user_update_event_handler(_id)
run()
