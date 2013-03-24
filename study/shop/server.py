#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from settings import *
import threading

# general good class
class GoodClass:
    def __init__(self, quantity, good_name = "Unknown"):
        self.good_name = good_name
        self.quantity = quantity

    def buyIt(self, quantity2buy):
        try:
            self.numquantity2buy = float(quantity2buy)
            if self.quantity >= self.numquantity2buy:
                self.quantity -= self.numquantity2buy
                self.text2return = "Thanks for your purchase!"
            else:
                self.text2return = "Sorry: there are no enough " + self.good_name + ". " + str(self.quantity) + " of " + self.good_name + " left over."
        except ValueError:
            self.text2return = "Sorry: couldn't buy " + quantity2buy + " of " + self.good_name + "."
        return(self.text2return)

# specific good classes
class Apple(GoodClass):
    def __init__(self, quantity, good_name = "Apple"):
        self.good_name = good_name
        self.quantity = quantity

class Banana(GoodClass):
    def __init__(self, quantity, good_name = "Banana"):
        self.good_name = good_name
        self.quantity = quantity

class Lemon(GoodClass):
    def __init__(self, quantity, good_name = "Lemon"):
        self.good_name = good_name
        self.quantity = quantity

class Orange(GoodClass):
    def __init__(self, quantity, good_name = "Orange"):
        self.good_name = good_name
        self.quantity = quantity

# socket connection thread class
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
                    self.text2return += "\n" + self.i.good_name + "\t" + str(self.i.quantity)
                self.sock.send("You could buy:" + self.text2return)
                    

            elif self.socket_buffer == "HELP":
                self.sock.send("Out shopping platform supports\nBUY good quantity\tbuy selected quantity of the good\nGET\t\t\tget goods list\nHELP\t\t\tget this help\nSETNAME nick\t\tlogin to your account\nME\t\t\tget current account name\nEXIT\t\t\tleave the shopping platform.")

            elif self.socket_buffer == "ME":
                self.sock.send(self.name)

            elif self.socket_buffer.startswith("BUY "):
                self.list2buy = self.socket_buffer.split(" ")
                self.text2return = ""
                for self.i in goods2sell:
                    if self.i.good_name == self.list2buy[1]:
                        try:
                            self.text2return = self.i.buyIt(self.list2buy[2])
                        except IndexError:
                            self.text2return = self.i.buyIt("1")
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
banana = Banana(5.4)
goods2sell.append(banana)
orange = Orange(7)
goods2sell.append(orange)
apple = Apple(11.1)
goods2sell.append(apple)
lemon = Lemon(2)
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
