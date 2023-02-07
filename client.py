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


# def check_dupname():




def login():
    client.send('LOGIN'.encode('ascii'))
    os.system("cls||clear")
    global username
    global password
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    
    


def signup():  
    os.system('cls||clear')
    # check if username is unique
    global username
    global password
    while True:
        try:
            username = input("Create your username: ")
            # send the username to server for duplicate check
            client.send(('SIGNUP '+username).encode('ascii'))
            dup_message = client.recv(1024).decode('ascii')
            if dup_message == "DUPNAME":
                print("Username already exists! Change to another one.")
            elif dup_message == "NONDUPNAME":
                password = input("Create your password: ")
                client.send(password.encode('ascii'))
                break

        except Exception as e:
            print('Error Occurred: ', e)
            client.close()
        

    
def listAccounts():
    # list all or a subset of the accounts by text wildcard
    # TODO
    os.system('cls||clear')
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
                        print("Wrong password! Try again")
                        stop = True
                    # elif :
                    #     # TODO
                # elif next_message == 'DUPNAME':
            elif message == "FAIL":
                print("You've reach the attemp limit, connection failed.")
            else: 
                print(message)
        except Exception as e:
            print('Error Occurred: ', e)
            client.close()
            break
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
    recieve_thread = threading.Thread(target=receive)
    recieve_thread.start()


def main():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the host
    client.connect((host, port))
    os.system("cls||clear")
    choose_operations()




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


