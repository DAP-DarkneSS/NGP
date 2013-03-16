#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import socket
from echo_stt import *
import logging
from os import makedirs, path
from os.path import exists, getmtime
from time import ctime

data_path = path.dirname(__file__) + "/data/"

logging.basicConfig(filename='example.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

sms = "Starting on host " + str(host) + " at port " + str(port)
print(sms)
logging.debug(sms)

sock, addr = s.accept()

id = ""
name = "Anonim"
if not exists(data_path):
    makedirs(data_path)
f = open((data_path + name + '.txt'), 'a+')

life = True
while life:
    buf = sock.recv(1024)
    logging.info(id + "-" + buf)

    if buf == "exit":
        sock.send("bye")
        sms = id + " became offline."
        print(sms)
        logging.debug(sms)
        life = False

    elif buf == "/0":
        sock.send("Nope!")

    elif buf == "GET":
        f.seek(0)
        i = f.read()
        if i != "":
            sock.send(i)
        else:
            sock.send("Nothing to show :(")

    elif buf == "HELP":
        sock.send("Доступные команды:\nADD\tсохранить информацию на сервере\nGET\tвывести сохранённую информацию\nHELP\tпоказать эту справку\nNAME\tавторизация\nME\tвывести имя текущего пользователя\nexit\tвыход.")

    elif buf == "ME":
        sock.send(name)

    elif buf.startswith("ADD "):
        i = buf.split(" ", 1)
        f.seek(0, 2)
        f.write(i[1] + "\n")
        sock.send("Done.")

    elif buf.startswith("CID "):
        i = buf.split(" ", 1)
        id = i[1]
        sms = id + " became online!"
        print(sms)
        logging.debug(sms)
        sock.send("Ты подключился к серверу МЕГАСЕРВЕР. Справка по командам доступка по запросу HELP")

    elif buf.startswith("NAME "):
        i = buf.split(" ", 1)
        name = i[1]

        filename = data_path + name + '.txt'
        try:
            if open(filename):
                last_time = "\nYour last note was made at " + str(ctime(getmtime(filename)))
        except (IOError, NameError):
            last_time = ""

        f.close()
        f = open((data_path + name + '.txt'), 'a+')

        sock.send("Hello, " + name + "!" + last_time)

    elif buf:
        sock.send(buf)

sms = "Exiting."
print(sms)
logging.debug(sms)
sock.close()
