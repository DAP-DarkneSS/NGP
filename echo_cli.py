#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import socket
from echo_stt import *

id = "rabbit"
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send("CID " + id)
result = s.recv(1024)
print result
life = True
while life:
    buf = raw_input(">>")
    if buf.startswith("CID "):
        print("Запрещено.")
    else:
        s.send(buf)
        result = s.recv(1024)
        print result
    if buf == "exit":
        life = False
s.close()
