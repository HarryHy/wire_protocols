import threading
import socket
import json

host = "100.91.14.32"
port = 5555
# keep a set of already logged in users
logins = set()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print('Listening...')

def receive():
    while True:
        # connect with the client
        client, addr = server.accept()
        print(f"Connected with {str(addr)}")
        # ask the client for the username
        client.send("USERNAME".encode('ascii'))
        username = client.recv(1024).decode('ascii')
        client.send('PASSWORD'.encode('ascii'))
        password = client.recv(1024).decode('ascii')
        # check if password matches with user name
        with open('accounts.json') as f:
            data = json.load(f)
        if password != data[username]["password"]:
            client.send("REJECT".encode('ascii'))
            client.close()
            continue # returns the control to the beginning of the while loop
        else:
            print("Successfully logged in!")
            logins.add(username)



receive()