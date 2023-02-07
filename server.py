import threading
import socket
import json

host = "100.91.14.32"
port = 5555
# keep a set of already logged in users
logins = set()
# keep a number of logged in times, exceeding this limit will cause break of the connection
LOGIN_LIMIT = 5
login_times = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print('Listening...')

def receive():
    # connect with the client
    client, addr = server.accept()
    print(f"Connected with {str(addr)}")
    while True:
        
        operation = client.recv(1024).decode('ascii')
        if operation == "LOGIN":
            login_times += 1
            if login_times > LOGIN_LIMIT:
                client.send("FAIL".encode('ascii'))
                client.close()

            # check whether username and password match
            # ask the client for the username
            client.send("USERNAME".encode('ascii'))
            username = client.recv(1024).decode('ascii')
            client.send('PASSWORD'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            # check if password matches with user name
            with open('accounts.json') as f:
                data = json.load(f)
            if password != data[username]["password"]:
                print("Login rejected!")
                client.send("REJECT".encode('ascii'))
                continue # returns the control to the beginning of the while loop
            else:
                print("Successfully logged in!")
                logins.add(username)
        elif operation.startswith("SIGNUP"):
            # check whether the username already exists
            username = operation.split(" ")[1]
            with open('accounts.json') as f:
                data = json.load(f)
            if username in data:
                client.send('DUPNAME'.encode('ascii'))
            else:
                client.send('NONDUPNAME'.encode('ascii'))
                password = client.recv(1024).decode('ascii')
                # store the new created account into the json file
                with open("accounts.json", "w") as f:
                    data[username] = {"password": password}
                    json.dump(data, f, indent=4)
            
        



receive()