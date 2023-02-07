import os
import threading
import socket
import json
import argparse
import fnmatch

# global variables
stop = False
username = "example"
password = "123"



def login():
    os.system("cls||clear")
    global username
    global password
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    # check the validy of the login at the server side
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to a host
    client.connect((host, port))


def signup():
    os.system('cls||clear')
    global username
    global password
    while True:
        username = input("Create your username: ")
        # check if username is unique
        with open("accounts.json", "r") as f:
            data = json.load(f)
        if username in data:
            print("Username already exists! Change to another one.")
        else:
            break
    password = input("Create your password: ")
    # store the new created account into the json file
    with open("accounts.json", "w") as f:
        data[username] = {"password": password}  # TODO: check both integers and strings work
        json.dump(data, f, indent=4)
    
def listAccounts():
    # list all or a subset of the accounts by text wildcard
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
        option = input("(1)Sign in\n(2)Sign up\n(3)List existing accounts\n")
        if option == "1":
            login()
            break
        elif option == "2":
            signup()
        elif option == "3":
            listAccounts()

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


