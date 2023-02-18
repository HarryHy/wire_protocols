import threading
from tkinter import *
from tkinter import simpledialog

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc

address = 'localhost'
port = 11912


class Client:

    def __init__(self, u: str, talkto: str, window):
        self.window = window
        self.username = u
        self.talkto = talkto
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        threading.Thread(target=self.__listen_for_messages,
                         daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()

    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for note in self.conn.ChatStream(chat.Empty()):  # this line will wait for new messages from the server!
            # print("[{}] R from [{}] {}".format(note.recipientname,
            #      note.sendername, note.message))  # debugging statement
            self.chat_list.insert(END, "[{}] to [{}] {}\n".format(
                note.sendername, note.recipientname, note.message))  # add the message to the UI

    def send_message(self, event):
        """
        This method is called when user enters something into the textbox
        """
        message = self.entry_message.get()  # retrieve message from the UI
        if message != '':
            n = chat.Note()  # create protobug message (called Note)
            n.sendername = self.username  # set the username
            n.recipientname = self.talkto
            n.message = message  # set the actual message of the note
            # print("[{}] S to [{}] {}".format(n.sendername,
            #      n.recipientname, n.message))
            self.conn.SendNote(n)  # send the Note to the server

    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)


def login():
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    n = chat.LoginRequest()
    n.username = username
    n.password = password
    channel = grpc.insecure_channel(address + ':' + str(port))
    conn = rpc.ChatServerStub(channel)
    print(conn.Login(n))


'''def signup():
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    n = chat.SignupRequest()
    n.username = username
    n.password = password
    channel = grpc.insecure_channel(address + ':' + str(port))
    conn = rpc.ChatServerStub(channel)
    print(conn.Login(n))'''


def choose_operations():
    while True:
        option = input(
            "(1)Sign in\n(2)Sign up\n(3)List existing accounts\n(4)Exit\n")
        if option == "1":  # TODO
            login()
            break
        elif option == "2":
            # signup()
            break
        elif option == "3":
            print("listAccounts")
        elif option == "4":
            return
        else:
            print("Invalid option, choose again")


if __name__ == '__main__':
    root = Tk() 
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    choose_operations()
    username = 'system'
    talkto = 'test'
    root.deiconify()
    c = Client(username, talkto, frame)

    # while username is None:
    # retrieve a username so we can distinguish all the different clients
    #    username = simpledialog.askstring(
    #        "Username", "What's your username?", parent=root)
    # while talkto is None:
    #    talkto = simpledialog.askstring(
    #        "Talkto", "Who do you want to talk to?", parent=root)
