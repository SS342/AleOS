from rich.progress import track
import os
import sys
import time
import threading

os.system("cls")
os.system("title " + "AleOS")

for step in track(range(20), description="Loading..."):
    time.sleep(0.1)

print(
'''
░█████╗░██╗░░░░░███████╗░█████╗░░██████╗
██╔══██╗██║░░░░░██╔════╝██╔══██╗██╔════╝
███████║██║░░░░░█████╗░░██║░░██║╚█████╗░
██╔══██║██║░░░░░██╔══╝░░██║░░██║░╚═══██╗
██║░░██║███████╗███████╗╚█████╔╝██████╔╝
╚═╝░░╚═╝╚══════╝╚══════╝░╚════╝░╚═════╝░
'''
)

def StartVKos():
    os.system("py UserNetworkMonitoring\\VK\\mainVK.py")

def StartTGos():
    os.system("py UserNetworkMonitoring\\TG\\mainTG.py")

VKos = threading.Thread(target=StartVKos)
TGos = threading.Thread(target=StartTGos)

VKos.start()
TGos.start()



