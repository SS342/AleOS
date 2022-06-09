import configparser
import locale
import os
import sys
import threading
import time

from rich.progress import track

os.environ["PYTHONIOENCODING"] = "utf-8"
thisLocale = locale.setlocale(category=locale.LC_ALL, locale="en_GB.UTF-8")
config = configparser.ConfigParser()
config.read('config.ini')
os.system("cls") if "win" in str(sys.platform) else ""
os.system("title " + "AleOS") if "win" in str(sys.platform) else ""

for step in track(range(20), description="Loading..."):
    time.sleep(0.1)


#
def Start_VKos():
    os.system("py UserNetworkMonitoring\\VK\\mainVK.py") if "win" in str(sys.platform) else os.system(
        "python3 UserNetworkMonitoring/VK/mainVK.py")


def do(command):
    if command == "sql":
        if input("vk or tg: ").lower() == "vk":
            pass
        else:
            print(command.upper())
    else:
        if 'wait' in command:
            print(f"Wait for {command.split()[1]} s.")
            time.sleep(int(command.split()[1]))
        else:
            print(command.upper())


def listen_command():
    time.sleep(60)
    while True:
        command = input("$ ")
        do(command.lower())
        time.sleep(0.5)


print(f"Python version: {config['Script']['PytVersion']}")
print(f"Author: {config['Script']['author']}")
print(f"Script version: {config['Script']['v']}")

VKos = threading.Thread(target=Start_VKos)
CommandOS = threading.Thread(target=listen_command)

VKos.start()
CommandOS.start()
