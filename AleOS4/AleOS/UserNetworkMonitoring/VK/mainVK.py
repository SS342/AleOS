# -*- coding: utf-8 -*-

import configparser
import logging
import sqlite3
import sys
import time

from requests_html import HTMLSession
from rich.console import Console
from rich.logging import RichHandler

config = configparser.ConfigParser()
config.read('config.ini')

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logging.disable(level=logging.DEBUG)
log_rich = logging.getLogger("rich")

Error001: str = "Error001"  # db list out of range

console = Console()
vk_api_link = str(config['VKos']['vk_api_link'])
access_token = str(config['VKos']['access_token'])
v = str(config['VKos']['v'])

log_rich.info(f"[ AleOS-vk ] : VK API link: {vk_api_link}")
log_rich.info(f"[ AleOS-vk ] : Access token: {access_token}")
log_rich.info(f"[ AleOS-vk ] : version : {v}")

log_rich.info(f"[ AleOS-vk ] : Извлечение пользовательских id")
path = "UserNetworkMonitoring\\VK\\usr.txt" if "win" in str(sys.platform) else "UserNetworkMonitoring/VK/usr.txt"
with open(path, "r") as usr:
    users = [line.rstrip().split("|")[0] for line in usr]
#  print(users)
num_of_user = 1

db = None


def log(stats: dict) -> None:
    '''Функция для выведения иформации в консоль'''
    text = f"[ AleOS-vk ] : {stats['name']} {'В сети' if stats['status'] == 'online' else 'Не в сети'} {stats['device'] if stats['status'] == 'online' else ''} {stats['time']}"
    console.log(text, log_locals=False)


class DataBase(object):
    '''Класс для работы с базой данных'''
    def __init__(self):
        """Инициализация класса"""
        if "win" in str(sys.platform):
            self.connection = sqlite3.connect(
                "UserNetworkMonitoring\\VK\\users.db" if __name__ == '__main__' else "users.db")
        else:
            self.connection = sqlite3.connect(
                "UserNetworkMonitoring/VK/users.db" if __name__ == '__main__' else "users.db")
        self.cursor = self.connection.cursor()

    def create_table(self) -> None:
        """Создание таблиц в базе данных"""
        sql = "CREATE TABLE IF NOT EXISTS users(name STRING, device STRING,status STRING, time STRING);"
        self.cursor.execute(sql)
        self.connection.commit()

    def get_Last_Online(self, name: str, status: str) -> bool | str:
        """Проверка последнего статуса юзера"""
        try:
            return True if status == \
                           self.cursor.execute(f"SELECT status FROM users WHERE name = '{name}'").fetchall()[-1][
                               0] else False
        except:
            log_rich.error(Error001)
            return Error001

    def write_info(self, stats: dict) -> None:
        """Запись ифнормации в базу данных"""
        data = self.get_Last_Online(stats['name'], stats['status'])
        if not (data):
            self.update_user(stats)
            log(stats)
        elif (data) == Error001:
            self.update_user(stats)
            log(stats)

    def update_user(self, stats: dict) -> None:
        """Обновление информации в базе данных"""
        sql = f"INSERT INTO users values('{stats['name']}', '{stats['device']}', '{stats['status']}', '{stats['time']}')"
        self.cursor.execute(sql)
        self.connection.commit()


def err(error):
    if "win" in str(sys.platform):
        with open("UserNetworkMonitoring\\VK\\err.txt", "a") as ferr:
            ferr.write(str(error))
    else:
        with open("UserNetworkMonitoring/VK/err.txt", "a") as ferr:
            ferr.write(str(error))


def check_user(ids):
    DataBase_ = DataBase()
    DataBase_.create_table()

    get_link = vk_api_link + "users.get?user_ids=" + str(
        ids) + "&fields=sex,online,last_seen&access_token=" + access_token + "&v=" + v + "&lang=ru"

    content = HTMLSession().get(get_link)
    json = content.json()

    sex = [["была в сети", "был в сети"], ["в сети", "в сети"]]
    device = ["с мобильного", "с iPhone", "с iPad", "с Android", "с Windows Phone", "с Windows 10", "с ПК",
              "с VK Mobile"]

    for i in range(num_of_user):
        userinfo = json["response"][i]
        user_stat = userinfo["last_seen"]

        name_of_user = userinfo["first_name"] + " " + userinfo["last_name"]
        ms_time = time.gmtime(int(user_stat["time"]) + 10800)

        user_stat = {
            "name": name_of_user,
            "sex": sex[int(userinfo["online"])][int(userinfo["sex"]) - 1],
            'device': device[int(user_stat["platform"]) - 1],
            'time': time.strftime("%d %b %Y %H:%M:%S", ms_time),
            'status': 'online' if int(userinfo["online"]) else 'offline'
        }

        DataBase_.write_info(user_stat)


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
        for user in users:
            try:

                check_user(user)
            except Exception as e:
                err(f"{str(e)} {user}\n")

        time.sleep(60 * float(timer_delay))


run()
