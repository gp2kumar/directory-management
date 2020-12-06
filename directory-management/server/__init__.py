from tkinter import Tk, Label, Frame, Text, Button, messagebox, END
import os
import socket
import threading
import tempfile
import json
import shutil


class Server:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432
        self.server = None
        self.server_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_channel.bind((self.host, self.port))
        self.is_channel_availble = True
        self.connected_users = {}
        self.server_actions = {}
        self.file_system = tempfile.gettempdir()

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
        self.server_log.delete("1.0", END)
        self.server_log.insert("1.0",text+'\n')
        self.server_log.configure(state='disabled')

    def clear_server_actions(self):
        self.server_actions.clear()
        self.server_log.configure(state='normal')
        self.server_log.delete("1.0", END)
        self.server_log.configure(state='disabled')

    def add_to_connected_clients_log(self, text):
        self.connected_clients_log.configure(state='normal')
        self.connected_clients_log.delete("1.0", END)
        self.connected_clients_log.insert("1.0", text+'\n')
        self.connected_clients_log.configure(state='disabled')

    def close_server_connection(self):
        # messagebox.showwarning("Title", "Closing Server")
        try:
            self.server_channel.close()
        except Exception as e:
            print("Exception while closing the server connection - {}".format(str(e)))
        finally:
            self.is_channel_availble = False
            self.connected_users.clear()
            self.populate_connected_devices_log()
            self.clear_server_actions()

    def start_listening(self):
        listener = threading.Thread(target=self.start_serving_as_server)
        listener.start()

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

            thread_id = threading.Thread(target=self.on_new_client, args=(c, addr)).start()

    def on_new_client(self,clientsocket, addr):

        user = clientsocket.recv(1024).decode()

        # check whether threshold reached or not
        if len(self.connected_users) == 3:
            message = {}
            message["STATUS"] = "NOTCONNECTED"
            message["STATUS_MESSAGE"] = "USER_SESSIONS_REACHED_THRESHOLD"
            clientsocket.send(json.dumps(message).encode())
            # clientsocket.send("USER_SESSIONS_REACHED_THRESHOLD".encode())
            clientsocket.close()
            return
        # check a user session is already available or not
        elif user in self.connected_users:
            message = {}
            message["STATUS"] = "NOTCONNECTED"
            message["STATUS_MESSAGE"] = "USER_SESSION_AVAILBLE"
            clientsocket.send(json.dumps(message).encode())
            clientsocket.close()
            return
        else:
            self.connected_users[user] = (addr[0], addr[1])
            self.server_actions[user] = []
            self.populate_connected_devices_log()
            if os.path.exists(os.path.join(self.file_system, user)):
                print("{} home directory existed".format(user))
            else:
                os.makedirs(os.path.join(self.file_system, user))

            details = {"DATA": [{"display_name":  '/home/'+user,
                                 "full_path": os.path.join(self.file_system, user),
                                 "is_child_availble": bool([x for x in os.listdir(os.path.join(self.file_system, user))])
                                 }],
                       "STATUS": "CONNECTED"}
            clientsocket.send(json.dumps(details).encode())

        while True:
            try:
                msg = clientsocket.recv(1024)
                print(msg)
                if not self.is_channel_availble:
                    print("closing the connection for the client {}:{}".format(addr[0], addr[1]))
                    break
                incoming_message = {}
                if len(msg.decode()) >0:
                    incoming_message = json.loads(msg.decode())
                else:
                    break
                if incoming_message.get("TYPE") == 'DIRECTORY_DETAILS':
                    directory_details = self.get_directory_details(incoming_message["DIRECTORY_PATH"])
                    clientsocket.send(json.dumps(directory_details).encode())
                elif incoming_message.get("TYPE") == 'CREATE_DIRECTORY':
                    try:
                        os.mkdir(incoming_message["directory_to_be_created"])
                    except FileExistsError:
                        pass

                    message = {}
                    message['STATUS'] = 'FAIL'
                    if os.path.exists(incoming_message["directory_to_be_created"]):
                        actions = {'command': 'os.mkdir("{}")'.format(incoming_message["directory_to_be_created"]),
                                   'log_message': '{} : {} created successfully'.format(user, incoming_message[
                                       "directory_to_be_created"]),
                                   'redo_command': 'shutil.rmtree(r"{}")'.format(
                                       incoming_message["directory_to_be_created"])}
                        self.server_actions[user].append(actions)
                        message['STATUS'] = 'SUCCESS'

                    clientsocket.send(json.dumps(message).encode())
                elif incoming_message.get("TYPE") == 'DELETE_DIRECTORY':
                    shutil.rmtree(incoming_message["directory_to_be_deleted"])
                    message = {}
                    message['STATUS'] = 'FAIL'
                    if not os.path.exists(incoming_message["directory_to_be_deleted"]):
                        actions = {'command': 'shutil.rmtree("{}")'.format(
                                       incoming_message["directory_to_be_deleted"]),
                                   'log_message': '{} : {} deleted successfully'.format(user, incoming_message[
                                       "directory_to_be_deleted"]),
                                   'redo_command': 'os.mkdir(r"{}")'.format(incoming_message["directory_to_be_deleted"])}
                        self.server_actions[user].append(actions)
                        message['STATUS'] = 'SUCCESS'

                    clientsocket.send(json.dumps(message).encode())
                elif incoming_message.get("TYPE") == 'RENAME_DIRECTORY':
                    p = incoming_message.get("directory")
                    parent_directory = os.path.dirname(p)
                    existing_directory = os.path.basename(p)
                    new_name = incoming_message.get("directory_to_be_renamed")
                    old_directory = os.path.join(parent_directory, existing_directory)
                    new_directory = os.path.join(parent_directory, new_name)
                    os.rename(old_directory, new_directory)
                    message = {}
                    message['STATUS'] = 'FAIL'
                    if os.path.exists(os.path.join(parent_directory,new_name)):
                        actions = {'command': 'os.rename({}, {})'.format(old_directory, new_directory),
                                   'log_message': '{} renamed to {} deleted successfully'.format(old_directory, new_directory),
                                   'redo_command': 'os.rename(r"{}", r"{}")'.format(new_directory, old_directory)}
                        self.server_actions[user].append(actions)
                        message['STATUS'] = 'SUCCESS'

                    clientsocket.send(json.dumps(message).encode())
                elif incoming_message.get("TYPE") == 'UNDO':
                    message = {}
                    if self.server_actions[user]:
                        last_action = self.server_actions[user].pop()
                        exec(last_action['redo_command'])
                        message['STATUS'] = 'SUCCESS'
                        # if not os.path.exists(incoming_message["directory_to_be_deleted"]):
                        #     actions = {'command': 'shutil.rmtree({})'.format(
                        #                    incoming_message["directory_to_be_deleted"]),
                        #                'log_message': '{} : {} deleted successfully'.format(user, incoming_message[
                        #                    "directory_to_be_deleted"]),
                        #                'redo_command': 'os.mkdir({})'.format(incoming_message["directory_to_be_deleted"])}
                        #     self.server_actions[user].append(actions)
                        #     message['STATUS'] = 'SUCCESS'
                    else:
                        message['STATUS'] = 'NOTHING_TO_UNDO'

                    clientsocket.send(json.dumps(message).encode())

                log_message = ""
                for user in self.server_actions:
                    for act in self.server_actions[user]:
                        log_message = act['log_message']+"\n"+log_message

                self.add_to_server_log(log_message)
                # new_message_from_server = "server: "+msg.decode()

            except ConnectionResetError:
                print("Remote client closed the connection")
                break
            except ConnectionAbortedError:
                print("Remote client disconnected")
                break
        clientsocket.close()
        # when server closes, all connected users are removing at other place. So, check before removing
        if user in self.connected_users:
            del self.connected_users[user]
        self.populate_connected_devices_log()

    def populate_connected_devices_log(self):
        connected_users = ""
        for user, address in self.connected_users.items():
            connected_users = connected_users + "{}, {}:{} connected\n".format(user, address[0], address[1])
        self.add_to_connected_clients_log(connected_users)

    def get_directory_details(self, directory):
        directory_contents = []
        for file in os.listdir(directory):
            file_details = {}
            file_details["display_name"] = file
            file_details["full_path"] = os.path.join(directory, file)
            if not os.path.isdir(os.path.join(directory, file)):
                file_details["is_child_availble"] = False
            elif [x for x in os.listdir(os.path.join(directory,file))]:
                file_details["is_child_availble"] = True
            else:
                file_details["is_child_availble"] = False

            directory_contents.append(file_details)
        return directory_contents
