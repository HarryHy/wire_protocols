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

 
    global username
    global password
    username = input("Enter the username:")
    password = input("Enter the password: ")
    # check the validy of the login at the server side
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to a host
    client.connect((host, port))
    client.send('login'.encode('ascii'))

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

        print("login successfully")
        return

def signup():
    os.system("cls||clear")
    # load all accounts

    global username
    global password
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to a host
    client.connect((host, port))

    try:
        client.send('signup'.encode('ascii'))

        username = input("Create a username:")
        client.send(username.encode('ascii'))
        message = client.recv(1024).decode('ascii')
        print(message)
        if message == "USERNAME":
            next_message = client.recv(1024).decode('ascii')
            
            if next_message == 'PASSWORD':
                print("2")
                password = input("Create the password: ")
                client.send(password.encode('ascii'))
                print("sign up successfully")
            elif next_message == "INVALID": 
                print("Invalid username")
                retry = input("Retry ? y/n")
                if retry is "y":
                    signup()
                else:
                    return


    except Exception as e:
        print('Error Occurred: ', e)
        client.close()
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
            break
    print("start to chat")
    #recieve_thread = threading.Thread(target=receive)
    #recieve_thread.start()


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-u', dest = 'host' , help = '172.16.225.218')
    parse.add_argument('-p', dest = 'port' ,type=int,help = '9999')
    args = parse.parse_args()
    global host 
    global port 
    host = args.host
    port = args.port
    main()


