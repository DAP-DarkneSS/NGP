#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from settings import *
import logging
from time import ctime
import os
import threading

# logging settings
logging.basicConfig(filename='example.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# create empty dirs
data_path = os.path.dirname(os.path.realpath(__file__)) + "/data/"
if not os.path.exists(data_path):
    os.makedirs(data_path)

# initial client ID
client_id = 0;
message2send = "Starting on host " + str(host) + " at port " + str(port)
print(message2send)
logging.debug(message2send)

class Connect(threading.Thread):
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        threading.Thread.__init__(self)

    def run (self):
        global client_id
        global logging
        #global global_life

        self.name = "Anonim"
        self.life = True

        while self.life:
            self.socket_buffer = self.sock.recv(1024)
            logging.info(self.name + " - " + self.socket_buffer)

            if self.socket_buffer == "exit":
                self.sock.send("bye")
                self.message2send = self.name + " became offline."
                print(self.message2send)
                logging.debug(self.message2send)
                self.life = False

            elif self.socket_buffer == "/0":
                self.sock.send("Nope!")

            elif self.socket_buffer == "CONNECT":
                client_id += 1
                self.message2send = self.name + " became online!"
                self.filename = data_path + self.name + '.txt'
                self.file = open((data_path + self.name + '.txt'), 'a+')
                self.file.close()

                print(self.message2send)
                logging.debug(self.message2send)
                self.sock.send("Ты подключился к серверу МЕГАСЕРВЕР. Справка по командам доступка по запросу HELP\nТвое имя - " + self.name)

            elif self.socket_buffer == "GET":
                self.file = open((data_path + self.name + '.txt'), 'a+')
                self.file.seek(0)
                self.file_content = self.file.read()
                if self.file_content != "":
                    self.sock.send(self.file_content)
                else:
                    self.sock.send("Nothing to show :(")
                self.file.close()

            elif self.socket_buffer == "HALT":
                self.sock.send("Not implemented :(")
                #self.sock.send("Close all connections to shutdown the server.")
                global_life = False

            elif self.socket_buffer == "HELP":
                self.sock.send("Доступные команды:\nADD\tсохранить информацию на сервере\nGET\tвывести сохранённую информацию\nHALT\tвыключить сервер после завершения всех сеансов\nHELP\tпоказать эту справку\nSETNAME\tавторизация\nME\tвывести имя текущего пользователя\nexit\tвыход.")

            elif self.socket_buffer == "ME":
                self.sock.send(self.name)

            elif self.socket_buffer.startswith("ADD "):
                self.list2add = self.socket_buffer.split(" ", 1)
                self.file = open((data_path + self.name + '.txt'), 'a+')
                self.file.seek(0, 2)
                self.file.write(self.list2add[1] + "\n")
                self.file.close()
                self.sock.send("Done.")

            elif self.socket_buffer.startswith("SETNAME "):
                self.list2name = self.socket_buffer.split(" ", 1)
                self.name = self.list2name[1]
                self.message2send = self.name + " became online!"
                print(self.message2send)
                logging.debug(self.message2send)
                self.filename = data_path + self.name + '.txt'

                try:
                    if open(self.filename):
                        self.last_time = "\nYour last note was made at " + str(ctime(os.path.getmtime(self.filename)))
                except (IOError, NameError):
                    self.last_time = ""

                self.file = open((data_path + self.name + '.txt'), 'a+')
                self.file.close()
                self.sock.send("Hello, " + self.name + "!" + self.last_time)

            elif self.socket_buffer:
                self.sock.send(self.socket_buffer)

# close the socket at the end
        client_id -= 1
        self.sock.close()

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

# accept connections in threads
global_life = True
while global_life:
    sock, addr = s.accept()
    Connect(sock, addr).start()

message2send = "Exiting."
print(message2send)
logging.debug(message2send)
