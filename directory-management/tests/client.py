#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(1)
    print ("establishing connection")
    s.connect((HOST, PORT))
    print("established connection")
    s.settimeout(None)
    while True:
        inp = input()
        s.sendall(inp.encode())
        if inp == 'client_close':
            break
        data = s.recv(1024)
        print("data recieved is {}".format(str(data)))
    s.close()


