import os
import threading
import socket
import argparse
import pickle
lock = threading.Lock()

clear = os.system("cls||clear")
# global variables
stop = False
username = "example"
password = "123"
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

# def check_dupname():

def login():
    client.send('LOGIN'.encode('ascii'))
    os.system("cls||clear")
    global username
    global password
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    global stop
    stop = False
    
    


def signup():  
    os.system('cls||clear')
    # check if username is unique
    global username
    global password
    while True:
        try:
            username = input("Create your username: ")
            # send the username to server for duplicate check
            print("signup 1")
            client.send(('SIGNUP '+username).encode('ascii'))
            dup_message = client.recv(1024).decode('ascii')
            print("signup 2")
            if dup_message == "DUPNAME":
                print("Username already exists! Change to another one.")
            elif dup_message == "NONDUPNAME":
                #id = username+current_time
                #client.send(id.encode('ascii'))
                password = input("Create your password: ")
                client.send(password.encode('ascii'))
                break

        except Exception as e:
            print('Error Occurred: ', e)

        

    
def listAccounts():
    os.system('cls||clear')
    # list all or a subset of the accounts by text wildcard
    while True:
        option = input("(1)List all \n(2)List by wildcard\n")
        if option == "1":
            client.send('LIST ALL'.encode('ascii'))
            break
        elif option == "2":
            pattern = input("Input your search pattern: ")
            client.send(('LIST '+pattern).encode('ascii'))
            break
        else: 
            print("Invalid option, choose again")
    
    response = client.recv(1024).decode('ascii')
    if response == "NOMATCHED":
        print("No matched account found")
    elif response == "MATCHED":
        client.send("SENDMATCHED".encode('ascii'))
        list_bytes = client.recv(4096)
        lock.acquire()
        list_accounts = pickle.loads(list_bytes)
        lock.release()
        for a in list_accounts:
            print(a)
        

def receive():
    print("in receive")
    try:
        while True:
            global stop
            if stop: break
            print("in loop")
        
            message = client.recv(1024).decode('ascii')
            # print("message is ", message)
            if message == "USERNAME":
                # print("client trying to send username")
                client.send(username.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASSWORD':
                    client.send(password.encode('ascii'))
                    check_state = client.recv(1024).decode('ascii')
                    if check_state == "REJECT":
                        print("Wrong password! Try again")
                        stop = True
                    elif check_state == "NOUSER":
                        print("No such user")
                        stop = True
                    else:
                        #print(s)
                        print("Successfully logged in as ", username)
                        return
            elif message == "FAIL":
                print("You've reach the attemp limit, connection failed.")
            else: 
                print(" the message is not on the list")
                print(message)
        print("out of while loop")
    except Exception as e:
        print('Error Occurred: ', e)
        if client:
            client.close()

    #client.send('RESTART'.encode('ascii'))
    choose_operations()

def choose_operations():
    while True:
        option = input("(1)Sign in\n(2)Sign up\n(3)List existing accounts\n")
        if option == "1":
            login()
            break
        elif option == "2":
            signup()
        elif option == "3":
            listAccounts()
        else: 
            print("Invalid option, choose again")
    # recieve_thread = threading.Thread(target=receive)
    # recieve_thread.start()
    receive()
    # recieve_thread.join()

def choose_talkto():
    print("please choose who to talk to")
    choose_talk_to_stop = False
    while True:
        if choose_talk_to_stop: 
            break
        global talkto
        talkto = input("Who do you want to talk to? (specify the username) ")
        client.send(("TALKTO "+talkto).encode('ascii'))
        next_message_bytes = client.recv(1024)
        try:
            next_message = next_message_bytes.decode('ascii')
            print("inside try is ", next_message)
            if next_message.startswith("CHATNOW"):
                print("the other user has already sent you a CHATNOW message before you specify him as the talkto")
            # message should be "VALTALKTO"
            # assert next_message == "VALTALKTO", "message should be VALTALKTO"
            print("Start your conversation with "+talkto + "!")
            choose_talk_to_stop = True
            break
        except:
            print("The username you were trying to talk to doesn't exist, please try another one. The available users are: \n")
            lock.acquire()
            list_accounts = pickle.loads(next_message_bytes)
            lock.release()
            for a in list_accounts:
                print(a)


        # next_message = client.recv(1024).decode('ascii')  # error: 'ascii' codec can't decode byte
        # if next_message == "VALTALKTO":
        #     print("Start your conversation with "+talkto + "!")
        #     choose_talk_to_stop = True
        #     break
        # else:
        #     print("The username you were trying to talk to doesn't exist, please try another one. The available users are: \n")
        #     list_accounts = pickle.loads(next_message.encode('ascii'))
        #     for a in list_accounts:
        #         print(a)

def start_conversation():
    #os.system('cls||clear')
    choose_talkto()
    client.send('STARTHIST'.encode('ascii'))
    # receive all the queued messages
    flag = client.recv(1024).decode('ascii')
    print("flag is ", flag)
    if flag != "EMPTY":
        list_bytes = client.recv(4096)
        #print("list_bytes is ", list_bytes)
        lock.acquire()
        list_messages = pickle.loads(list_bytes)
        lock.release()
        for m in list_messages:
            print(talkto + " : " + m)

    # if talkto hasn't specify you as the talkto, wait here until he has specified
    # print("Waiting here until talkto has talked to back......")
    # while True:
    #     client.send("ASKTALKTOBACK".encode("ascii"))
    #     response = client.recv(1024).decode('ascii')
    #     if response == "TALKTOBACK":
    #         break
    
    print("--------------the other user has talked to back! start to chat-----------------")
    # after receive the history, start to chat

    try:
        write_thread = threading.Thread(target=write_messages)
        write_thread.start()
        recieve_thread = threading.Thread(target=receive_messages)
        recieve_thread.start()

    except Exception as e:
        print('Error Occurred: ', e)
        write_thread.join()
        recieve_thread.join()
        if client:
            client.close()

class restart_conversation_exception(Exception):
    def __init__(self, message):
        print(message)

def write_messages():
    try:
        client.send('STARTCHAT'.encode('ascii'))

        chat_break = False
        while True:

            if chat_break:
                break
            
            input_message = input()
            if input_message == "\exit":
                chat_break = True
                client.send(('EXIT~' + talkto +"~" + username + "~"+ input_message).encode('ascii'))
                print("end of exit")
                return
            elif input_message == "\switch":
                chat_break = True
                client.send(('SWITCH~' + talkto +"~" + username + "~"+ input_message).encode('ascii'))
                print("end of switch")
                raise restart_conversation_exception("restart")
            else:
                print(username + " : " + input_message)
                client.send(('CHAT~' + talkto +"~" + username + "~"+ input_message).encode('ascii'))
    except restart_conversation_exception:
        start_conversation()
        return
    except Exception as e:
        print('Error Occurred: ', e)
        #client.close()

def receive_messages():
    online_flag = False
    omit_message = False
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message.startswith("CHATNOW"):
                if online_flag == False:
                    online_flag = True
                    print("this user is online now")
                    omit_message = False

                print(message[7:])
            elif message.startswith("CHATLATER"):
                online_flag = False
                if not omit_message:
                    print("this user is not online now, your message will not be received")
                omit_message = True
            elif message.startswith("EXIT"):
                return
            elif message.startswith("SWITCH"):
                global restart
                restart = True
                return    
        except Exception as e:
            print('Error Occurred: ', e)
            #client.close()







def main():
    try:
        os.system("cls||clear")
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the host
        client.connect((host, port))
        choose_operations()  # finished login here
        # recieve_thread = threading.Thread(target=start_conversation)
        # recieve_thread.start()
        start_conversation()
        # recieve_thread.join()
    except:
        if client:
            client.close()



if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-u', dest = 'host' , help = '127.0.0.1')
    parse.add_argument('-p', dest = 'port' ,type=int,help = '9999')
    args = parse.parse_args()
    global host
    global port
    #host = input("Enter the host: ")
    #port = input("Enter the port: ")

    host = args.host
    port = args.port
    main()


