#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from echo_stt import *
import logging
from time import ctime
import os

# logging settings
logging.basicConfig(filename='example.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# create empty dirs
data_path = os.path.dirname(os.path.realpath(__file__)) + "/data/"
if not os.path.exists(data_path):
    os.makedirs(data_path)

# default user
id = 0;
name = "Anonim"

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
sock, addr = s.accept()

#
sms = "Starting on host " + str(host) + " at port " + str(port)
print(sms)
logging.debug(sms)

life = True
while life:
    buf = sock.recv(1024)
    logging.info(name + " - " + buf)

    if buf == "exit":
        sock.send("bye")
        sms = name + " became offline."
        print(sms)
        logging.debug(sms)
        life = False

    elif buf == "/0":
        sock.send("Nope!")

    elif buf == "GET":
        f = open((data_path + name + '.txt'), 'a+')
        f.seek(0)
        i = f.read()
        if i != "":
            sock.send(i)
        else:
            sock.send("Nothing to show :(")
        f.close()

    elif buf == "HELP":
        sock.send("Доступные команды:\nADD\tсохранить информацию на сервере\nGET\tвывести сохранённую информацию\nHELP\tпоказать эту справку\nSETNAME\tавторизация\nME\tвывести имя текущего пользователя\nexit\tвыход.")

    elif buf == "ME":
        sock.send(name)

    elif buf.startswith("ADD "):
        i = buf.split(" ", 1)
        f = open((data_path + name + '.txt'), 'a+')
        f.seek(0, 2)
        f.write(i[1] + "\n")
        f.close()
        sock.send("Done.")

    elif buf.startswith("CONNECT"):
        id = id + 1
        sms = name + " became online!"
        filename = data_path + name + '.txt'
        f = open((data_path + name + '.txt'), 'a+')
        f.close()

        print(sms)
        logging.debug(sms)
        sock.send("Ты подключился к серверу МЕГАСЕРВЕР. Справка по командам доступка по запросу HELP\nТвое имя - " + name)

    elif buf.startswith("SETNAME "):
        i = buf.split(" ", 1)
        name = i[1]
        filename = data_path + name + '.txt'

        try:
            if open(filename):
                last_time = "\nYour last note was made at " + str(ctime(getmtime(filename)))
        except (IOError, NameError):
            last_time = ""

        f = open((data_path + name + '.txt'), 'a+')
        f.close()
        sock.send("Hello, " + name + "!" + last_time)

    elif buf:
        sock.send(buf)

sms = "Exiting."
print(sms)
logging.debug(sms)
sock.close()
