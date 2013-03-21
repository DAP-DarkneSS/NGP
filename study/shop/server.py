#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from settings import *
import threading

class GoodClass:
    def __init__(self, quantity):
        self.quantity = quantity

    def bueIt(self.mass = 1):
        if self.quantity >= self.mass:
            self.quantity -= self.mass
            return(True)
        else:
            return(False)

class Connect(threading.Thread):
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        threading.Thread.__init__(self)

    def run (self):

        self.name = "Anonim"
        self.life = True

        while self.life:
            self.socket_buffer = self.sock.recv(1024)

            if self.socket_buffer == "EXIT":
                self.sock.send("You've left the shop.")
                self.life = False

            elif self.socket_buffer == "CONNECT":
                self.sock.send("Welcome to Next Generation Shop. Type HELP to get help :) \nYou've logged as " + self.name + ".")

            elif self.socket_buffer == "GET":
                pass

            elif self.socket_buffer == "HELP":
                self.sock.send("Out shopping platform supports\nADD good\tadd selected good to your basket\nGET\t\tget goods list\nHELP\t\tget this help\nSETNAME nick\tlogin to your account\nME\t\tget current account name\nEXIT\t\tleave the shopping platform.")

            elif self.socket_buffer == "ME":
                self.sock.send(self.name)

            elif self.socket_buffer.startswith("ADD "):
                pass

            elif self.socket_buffer.startswith("SETNAME "):
                self.list2name = self.socket_buffer.split(" ", 1)
                self.name = self.list2name[1]
                self.sock.send("Hello, " + self.name + "!")

            elif self.socket_buffer:
                self.sock.send(self.socket_buffer)

# close the socket at the end
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

#message2send = "Exiting."
#print(message2send)
#logging.debug(message2send)
