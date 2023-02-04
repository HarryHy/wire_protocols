import os
import threading
import socket
import json
import argparse
# global variables
stop = False



def login():
    os.system("cls||clear")
    # load all accounts
    with open("accounts.json") as f:
        data = json.load(f)
 
    global username
    global password
    username = input("Enter the username:")
    password = input("Enter the password: ")
    # check the validy of the login at the server side
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to a host
    client.connect((host, port))


def signup():
    # TODO
    return



def receive():
    while True:
        global stop
        if stop: break
        try:
            message = client.recv(1024).decode('ascii')
            if message == "USERNAME":
                client.send(username.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASSWORD':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == "REJECT":
                        print("Wrong password!")
                        stop = True
                    # else:
                    #     # TODO
            else: 
                print(message)
        except Exception as e:
            print('Error Occurred: ', e)
            client.close()
            break

def main():
    while True:
        os.system("cls||clear")
        option = input("(1)Sign in\n(2)Sign up \n")
        if option == "1":
            login()
            break
        elif option == "2":
            signup()

    recieve_thread = threading.Thread(target=receive)
    recieve_thread.start()


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-u', dest = 'host' , help = '127.0.0.1')
    parse.add_argument('-p', dest = 'port' ,type=int,help = '9999')
    args = parse.parse_args()
    global host
    global port
    host = args.host
    port = args.port
    main()


