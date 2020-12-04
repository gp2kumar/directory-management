from tkinter import Tk, Label, Frame, Text, Button, messagebox
import os
import socket
import threading


class Server:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432
        self.server = None
        self.server_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_channel.bind((self.host, self.port))
        self.is_channel_availble = True

    def run(self):
        self.start_ui()
        self.start_listening()
        print("server started")
        self.server.mainloop()

    def configure_server_layout(self):
        self.server = Tk()
        self.server.title('Directory Management Server')
        self.server.minsize(800, 600)
        home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.server.iconbitmap(os.path.join(home_dir, "icon.ico"))

    def start_ui(self):
        self.configure_server_layout()
        self.attach_log_frame()
        self.attach_connected_clients_frame()
        self.attach_exit_button()

    def attach_log_frame(self):
        frame = Frame(self.server, width=500, height=600).place(x=0, y=0)
        Label(frame, text='Server Log', font='Helvetica 14 bold').place(x=50, y=8)
        self.server_log = Text(frame, state='disabled', width=50, height=30)
        self.server_log.place(x=20, y=50)

    def attach_connected_clients_frame(self):
        frame = Frame(self.server, width=250, height=600).place(x=510, y=0)
        Label(frame, text='Connected Clients', font='Helvetica 14 bold').place(x=550, y=10)
        self.connected_clients_log = Text(frame, state='disabled', width=25, height=10)
        self.connected_clients_log.place(x=535, y=50)

    def attach_exit_button(self):
        frame = Frame(self.server, width=200, height=200, bg="#ccc").place(x=510, y=650)
        self.exit_server = Button(frame, text="Exit Server", width=12, height=3, font='Helvetica 11 bold', command=self.close_server_connection)
        self.exit_server.place(x=565, y=465)

    def add_to_server_log(self, text):
        self.server_log.configure(state='normal')
        self.server_log.insert("1.0",text+'\n')
        self.server_log.configure(state='disabled')

    def add_to_connected_clients_log(self, text):
        self.connected_clients_log.configure(state='normal')
        self.connected_clients_log.insert("1.0", text+'\n')
        self.connected_clients_log.configure(state='disabled')

    def close_server_connection(self):
        messagebox.showwarning("Title", "Closing Server")
        try:
            self.server_channel.close()
        except Exception as e:
            print("Exception while closing the server connection - {}".format(str(e)))
        finally:
            self.is_channel_availble = False

    def start_serving_as_server(self):

        while True:
            # if threading.active_count() - 1 >= 2:
            #     continue
            self.server_channel.listen()
            try:
                c, addr = self.server_channel.accept()
            except OSError:
                print("Server connection is closed")
                break
            self.add_to_connected_clients_log("client {} connected from port {}".format(addr[0], addr[1]))
            threading.Thread(target=self.on_new_client, args=(c, addr)).start()

    def start_listening(self):
        listener = threading.Thread(target=self.start_serving_as_server)
        listener.start()

    def on_new_client(self,clientsocket, addr):
        while True:
            try:
                msg = clientsocket.recv(1024)
                if not self.is_channel_availble:
                    print("closing the connection for the client {}:{}".format(addr[0], addr[1]))
                    break
                self.add_to_server_log(msg.decode())
                new_message_from_server = "server: "+msg.decode()
                clientsocket.send(new_message_from_server.encode())
            except ConnectionResetError:
                print("Remote client closed the connection")
                break
        clientsocket.close()

