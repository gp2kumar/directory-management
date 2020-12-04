from tkinter import Tk, Label, Frame, Text, Button, messagebox
import os
import socket
import threading

class Client:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432
        self.client = None



    def run(self):
        self.start_ui()
        # self.start_listening()
        print("Client started")
        self.client.mainloop()

    def start_ui(self):
        self.configure_client_layout()
        self.attach_user_input_frame()
        self.attach_directory_viewer()
        self.attach_client_controls()

    def configure_client_layout(self):
        self.client = Tk()
        self.client.title('Directory Management Client')
        self.client.minsize(800, 600)
        home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.client.iconbitmap(os.path.join(home_dir, "icon.ico"))

    def attach_user_input_frame(self):
        frame = Frame(self.client, width=500, height=80, bg="#ccc").place(x=0, y=0)
        Label(frame, text='User Name', font='Helvetica 10 bold').place(x=50, y=19)
        self.client_user_name = Text(frame, state='normal', width=10, height=1)
        self.client_user_name.place(x=135, y=19)

    def attach_directory_viewer(self):
        frame = Frame(self.client, width=500, height=80, bg="#ddd").place(x=0, y=100)
        # Label(frame, text='User Name', font='Helvetica 10 bold').place(x=50, y=19)
        # self.client_user_name = Text(frame, state='normal', width=10, height=1)
        # self.client_user_name.place(x=135, y=19)

    def attach_client_controls(self):
        frame = Frame(self.client, width=500, height=600, bg="#aaa").place(x=510, y=0)
        self.connect = Button(frame, text="Connect", width=13, height=1, font='Helvetica 8 bold',
                                  command=self.connect_controller)
        self.connect.place(x=620, y=19)

        self.disconnect = Button(frame, text="Disconnect", width=13, height=1, font='Helvetica 8 bold',
                              command=self.disconnect_controller)
        self.disconnect.place(x=620, y=59)

        self.create_directory = Button(frame, text="Create Directory", width=13, height=1, font='Helvetica 8 bold',
                              command=self.create_directory_controller)
        self.create_directory.place(x=620, y=99)

        self.delete_directory = Button(frame, text="Delete Directory", width=13, height=1, font='Helvetica 8 bold',
                                       command=self.delete_directory_controller)
        self.delete_directory.place(x=620, y=139)

        self.move_directory = Button(frame, text="Move Directory", width=13, height=1, font='Helvetica 8 bold',
                                       command=self.move_directory_controller)
        self.move_directory.place(x=620, y=179)

        self.move_directory = Button(frame, text="Rename Directory", width=13, height=1, font='Helvetica 8 bold',
                                     command=self.rename_directory_controller)
        self.move_directory.place(x=620, y=219)

        self.sync = Button(frame, text="Sync", width=13, height=1, font='Helvetica 8 bold',
                                     command=self.sync_controller)
        self.sync.place(x=620, y=259)

    def connect_controller(self):
        self.client_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_channel.connect((self.host, self.port))
        self.client_channel.sendall(self.client_user_name.get("1.0",'end-1c').encode())
        self.is_channel_availble = True

    def disconnect_controller(self):
        self.client_channel.close()

    def create_directory_controller(self):
        pass

    def delete_directory_controller(self):
        pass

    def move_directory_controller(self):
        pass

    def rename_directory_controller(self):
        pass

    def sync_controller(self):
        pass