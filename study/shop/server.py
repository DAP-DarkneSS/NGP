#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from settings import *
import threading

class GoodClass:
    def __init__(self, good_name, quantity):
        self.good_name = good_name
        self.quantity = quantity

    def buyIt(self, quantity2buy = 1):
        if self.quantity >= quantity2buy:
            self.quantity -= quantity2buy
            return(True)
        else:
            return(False)

    def getName(self):
        return(self.good_name)

    def getQuantity(self):
        return(self.quantity)

class Connect(threading.Thread):
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        threading.Thread.__init__(self)

    def run (self):

        self.name = "Anonim"
        self.life = True

        global goods2sell

        while self.life:
            self.socket_buffer = self.sock.recv(1024)

            if self.socket_buffer == "EXIT":
                self.sock.send("You've left the shop.")
                self.life = False

            elif self.socket_buffer == "CONNECT":
                self.sock.send("Welcome to Next Generation Shop. Type HELP to get help :) \nYou've logged as " + self.name + ".")

            elif self.socket_buffer == "GET":
                self.text2return = ""
                for self.i in goods2sell:
                    self.text2return += "\n" + self.i.getName() + "\t" + str(self.i.getQuantity())
                self.sock.send("You could buy:" + self.text2return)
                    

            elif self.socket_buffer == "HELP":
                self.sock.send("Out shopping platform supports\nBUY good quantity\tbuy selected quantity of the good\nGET\t\t\tget goods list\nHELP\t\t\tget this help\nSETNAME nick\t\tlogin to your account\nME\t\t\tget current account name\nEXIT\t\t\tleave the shopping platform.")

            elif self.socket_buffer == "ME":
                self.sock.send(self.name)

            elif self.socket_buffer.startswith("BUY "):
                self.list2buy = self.socket_buffer.split(" ")
                self.text2return = ""
                for self.i in goods2sell:
                    if self.i.getName() == self.list2buy[1]:
                        try:
                            if self.i.buyIt(float(self.list2buy[2])):
                                self.text2return = "Thanks for your purchase!"
                            else:
                                self.text2return = "Sorry: there are no enough " + self.list2buy[1] + ". " + str(self.i.getQuantity()) + " of " + self.list2buy[1] + " left over."
                        except ValueError:
                            self.text2return = "Sorry: couldn't buy " + self.list2buy[2] + " of " + self.list2buy[1] + "."
                if self.text2return != "":
                    self.sock.send(self.text2return)
                else:
                    self.sock.send("Sorry: there are no such good. Use GET to get goods list.")

            elif self.socket_buffer.startswith("SETNAME "):
                self.list2name = self.socket_buffer.split(" ", 1)
                self.name = self.list2name[1]
                self.sock.send("Hello, " + self.name + "!")

            elif self.socket_buffer:
                self.sock.send(self.socket_buffer)

# close the socket at the end
        self.sock.close()

# add googs to sell
goods2sell =[]
banana = GoodClass("banana", 5.4)
goods2sell.append(banana)
orange = GoodClass("orange", 7)
goods2sell.append(orange)
apple = GoodClass("apple", 11.1)
goods2sell.append(apple)
lemon = GoodClass("lemon", 2)
goods2sell.append(lemon)

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
