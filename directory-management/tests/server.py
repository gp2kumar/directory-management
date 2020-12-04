import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def on_new_client(clientsocket,addr):
    print("inside new client")
    while True:

        msg = clientsocket.recv(1024)
        if msg.decode() == 'client_close':
            print("closing the connection")
            break
        print(addr, ' >> ', msg)
        msg = input('SERVER >> ')
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        clientsocket.send(msg.encode())
    clientsocket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    # conn, addr = s.accept()
    no_of_connections = 0

    while True:
        if threading.active_count()-1 >=2:
           continue
        s.listen()
        c, addr = s.accept()  # Establish connection with client.
        print('Connected by', addr)
        print("about to trigger a thread")
        threading.Thread(target = on_new_client, args = (c, addr)).start()
        print("triggered a thread")
    s.close()