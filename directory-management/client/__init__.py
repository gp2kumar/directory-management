from tkinter import Tk, Label, Frame, Text, Button, messagebox, ttk, simpledialog
import os
import socket
import re
import json

class Client:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432
        self.client = None
        self.server_message_decoder = {"CONNECTED": "client successfully connected",
                                       "USER_SESSION_AVAILBLE": "User session already availble, can not connect",
                                       "CLIENT_DISCONNECTED": "client successfully dis-connected",
                                       "SERVER_NOT_AVAILBLE": "Server Not availble",
                                       "USER_SESSIONS_REACHED_THRESHOLD": "Connections on server reached threshold. Please re-try after some time!",
                                       "USERNAME_SPECIAL_CHARACTERS": "user name has some special characters, please correct.",
                                       "DIRECTORY_CREATION_SUCCESS": "Directory Created Successfully",
                                       "DIRECTORY_DELETION_SUCCESS": "Directory Deleted Successfully",
                                       "DIRECTORY_CREATION_FAILED": "Not able to create Directory",
                                       "DIRECTORY_DELETION_FAILED": "Not able to Deleted Directory",
                                       "UNDO_SUCCESS": "Undo Success",
                                       "NOTHING_TO_UNDO": "Nothing to Undo",
                                       "DIRECTORY_RENAME_SUCCESS": "Renamed Successfully",
                                       "DIRECTORY_RENAME_FAILED": "Renaming Directory Failed"
                                       }
        self.nodes = dict()

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
        frame = Frame(self.client, width=500, height=80).place(x=0, y=0)
        Label(frame, text='User Name', font='Helvetica 10 bold').place(x=50, y=19)
        self.client_user_name = Text(frame, state='normal', width=10, height=1)
        self.client_user_name.place(x=135, y=19)
        self.client_log_area = Label(frame, text='', font='Helvetica 9 ')
        self.client_log_area.place(x=150, y=49)

    def attach_directory_viewer(self):
        frame = Frame(self.client, width=500, height=400, bg="#ccc")
        frame.place(x=50, y=80)
        self.tree = ttk.Treeview(frame)
        self.tree.pack(fill='x') #place(x=100, y=500)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Directory Structure', anchor='w')
        #
        self.tree.grid()
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        # frame.grid()
        #
    def insert_node(self, parent, node_details):
        node = self.tree.insert(parent, 'end', text=node_details['display_name'], open=False)
        self.nodes[node] = node_details
        print("insert node", node, node_details, self.nodes)
        if node_details['is_child_availble']:
            self.tree.insert(node, 'end')

    def open_node(self, event):
        # print ("tree opened")
        node = self.tree.focus()
        node_details = self.nodes.get(node, None)
        print("node_details", node_details)
        # print("children", self.tree.get_children(node))
        print("node", node)
        print("nodes", self.nodes)
        try:
            self.tree.delete(self.tree.get_children(node))
        except Exception:
            pass
        message = {}
        message["TYPE"] = "DIRECTORY_DETAILS"
        message["DIRECTORY_PATH"] = node_details["full_path"]
        self.client_channel.sendall(json.dumps(message).encode())
        data = self.client_channel.recv(1024)
        files = json.loads(data)
        for f in files:
            self.insert_node(node, f)

    def attach_client_controls(self):
        frame = Frame(self.client, width=500, height=600).place(x=510, y=0)
        self.connect = Button(frame, text="Connect", width=13, height=1, font='Helvetica 8 bold',
                                  command=self.connect_controller)
        self.connect.place(x=620, y=19)

        self.disconnect = Button(frame, text="Disconnect", width=13, height=1, font='Helvetica 8 bold',
                              command=self.disconnect_controller)
        self.disconnect.place(x=620, y=59)

        self.create_directory = Button(frame, text="Create Directory", width=13, height=1, font='Helvetica 8 bold',
                              command=self.create_directory_controller)
        self.create_directory.place(x=620, y=199)

        self.delete_directory = Button(frame, text="Delete Directory", width=13, height=1, font='Helvetica 8 bold',
                                       command=self.delete_directory_controller)
        self.delete_directory.place(x=620, y=239)

        self.move_directory = Button(frame, text="Move Directory", width=13, height=1, font='Helvetica 8 bold',
                                       command=self.move_directory_controller)
        self.move_directory.place(x=620, y=279)

        self.move_directory = Button(frame, text="Rename Directory", width=13, height=1, font='Helvetica 8 bold',
                                     command=self.rename_directory_controller)
        self.move_directory.place(x=620, y=319)

        self.sync = Button(frame, text="Sync", width=13, height=1, font='Helvetica 8 bold',
                                     command=self.sync_controller)
        self.sync.place(x=620, y=359)

        self.undo = Button(frame, text="Undo", width=13, height=1, font='Helvetica 8 bold',
                           command=self.undo_controller)
        self.undo.place(x=620, y=399)

    def connect_controller(self):
        self.user_name = self.client_user_name.get("1.0",'end-1c')
        special_characters_pattern = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if special_characters_pattern.search(self.user_name):
            self.client_log_area.configure(text=self.server_message_decoder["USERNAME_SPECIAL_CHARACTERS"])
            return
        try:
            self.client_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_channel.connect((self.host, self.port))
            self.client_channel.sendall(self.user_name.encode())
            data = self.client_channel.recv(1024)
            details = json.loads(data.decode())
            print(details)
            if details["STATUS"] == 'CONNECTED':
                self.client_log_area.configure(text=self.server_message_decoder[details["STATUS"]])
                self.insert_node('', details["DATA"][0])
                self.tree.bind('<<TreeviewOpen>>', self.open_node)
                self.is_channel_availble = True
            else:
                self.client_log_area.configure(text=self.server_message_decoder[details["STATUS_MESSAGE"]])
        except ConnectionRefusedError:
            self.client_log_area.configure(text=self.server_message_decoder["SERVER_NOT_AVAILBLE"])

    def disconnect_controller(self):
        self.client_channel.close()
        self.client_log_area.configure(text=self.server_message_decoder["CLIENT_DISCONNECTED"])

    def create_directory_controller(self):
        directory_name = simpledialog.askstring(title="",
                                          prompt="Enter the directory name")
        node = self.tree.focus()
        parent_directory = self.nodes[node]['full_path']
        message = {}
        message['TYPE'] = 'CREATE_DIRECTORY'
        message['directory_to_be_created'] = os.path.join(parent_directory, directory_name)
        data = b''
        try:
            self.client_channel.sendall(json.dumps(message).encode())
            data = self.client_channel.recv(1024)
        except OSError:
            self.client_log_area.configure(text=self.server_message_decoder["SERVER_NOT_AVAILBLE"])
            return
        details = json.loads(data.decode())

        if details["STATUS"] == 'SUCCESS':
            self.client_log_area.configure(text=self.server_message_decoder["DIRECTORY_CREATION_SUCCESS"])
        else:
            self.client_log_area.configure(text=self.server_message_decoder["DIRECTORY_CREATION_FAILED"])

    def delete_directory_controller(self):
        node = self.tree.focus()
        directory = self.nodes[node]['full_path']
        message = {}
        message['TYPE'] = 'DELETE_DIRECTORY'
        message['directory_to_be_deleted'] = directory
        data = b''
        try:
            self.client_channel.sendall(json.dumps(message).encode())
            data = self.client_channel.recv(1024)
        except OSError:
            self.client_log_area.configure(text=self.server_message_decoder["SERVER_NOT_AVAILBLE"])
            return
        details = json.loads(data.decode())

        if details["STATUS"] == 'SUCCESS':
            self.client_log_area.configure(text=self.server_message_decoder["DIRECTORY_DELETION_SUCCESS"])
        else:
            self.client_log_area.configure(text=self.server_message_decoder["DIRECTORY_DELETION_FAILED"])

    def rename_directory_controller(self):
        node = self.tree.focus()
        directory = self.nodes[node]['full_path']
        new_directory_name = simpledialog.askstring(title="",
                                                prompt="Enter the new directory name")
        if new_directory_name:
            message = {}
            message['TYPE'] = 'RENAME_DIRECTORY'
            message['directory'] = directory
            message['directory_to_be_renamed'] = new_directory_name
            data = b''
            try:
                self.client_channel.sendall(json.dumps(message).encode())
                data = self.client_channel.recv(1024)
            except OSError:
                self.client_log_area.configure(text=self.server_message_decoder["SERVER_NOT_AVAILBLE"])
                return
            details = json.loads(data.decode())

            if details["STATUS"] == 'SUCCESS':
                self.client_log_area.configure(text=self.server_message_decoder["DIRECTORY_RENAME_SUCCESS"])
            else:
                self.client_log_area.configure(text=self.server_message_decoder["DIRECTORY_RENAME_FAILED"])

    def move_directory_controller(self):
        pass

    def sync_controller(self):
        pass

    def undo_controller(self):
        message = {}
        message['TYPE'] = 'UNDO'
        data = b''
        try:
            self.client_channel.sendall(json.dumps(message).encode())
            data = self.client_channel.recv(1024)
        except OSError:
            self.client_log_area.configure(text=self.server_message_decoder["SERVER_NOT_AVAILBLE"])
            return
        details = json.loads(data.decode())

        if details["STATUS"] == 'SUCCESS':
            self.client_log_area.configure(text=self.server_message_decoder["UNDO_SUCCESS"])
        elif details["STATUS"] == 'NOTHING_TO_UNDO':
            self.client_log_area.configure(text=self.server_message_decoder["NOTHING_TO_UNDO"])
