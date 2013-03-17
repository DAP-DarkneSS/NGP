#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from settings import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send("CONNECT")
result = s.recv(1024)
print result
life = True
while life:
    buf = raw_input(">>")
    if buf == "":
        print("Нечего отправлять :(")
    elif buf == "CONNECT":
        print("Запрещено.")
    else:
        s.send(buf)
        result = s.recv(1024)
        print result
    if buf == "exit":
        life = False
s.close()
