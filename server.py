import threading
import socket
import json

host = "10.250.183.6"
port = 5555
# keep a set of already logged in users
logins = set()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print('Listening...')

def receive():
    try:
        with open('accounts.json') as f:
            data = json.load(f)
        while True:
            # connect with the client
            client, addr = server.accept()
            print(f"Connected with {str(addr)}")
            # ask the client for the username
            #client.send("USERNAME".encode('ascii'))
            opt = client.recv(1024).decode('ascii')

            if opt == 'login':
                print("logging in ")
                client.send("USERNAME".encode('ascii'))
                username = client.recv(1024).decode('ascii')
                
                if client not in logins: # client is not log in before. 
                    client.send('PASSWORD'.encode('ascii'))
                    password = client.recv(1024).decode('ascii')

                    # check if not password matches with user name
                    if str(password) != str(data[username]["password"]):
                        client.send("REJECT".encode('ascii'))
                        client.close()
                        continue # returns the control to the beginning of the while loop
                    else:
                        print("Successfully logged in!")
                        client.send("Successfully logged in!".encode('ascii'))
                        logins.add(client)
                        client.close()
                        continue
            
            elif opt == 'signup':
                print("signup ")
                with open('accounts.json') as f:
                    data = json.load(f)

                client.send("USERNAME".encode('ascii'))
                username = client.recv(1024).decode('ascii')
                print('username is', username)
                print( list(data.keys()))
                if str(username) not in list(data.keys()): # client is not log in before. 
                    print("1")
                    client.send('PASSWORD'.encode('ascii'))
                    user_password = client.recv(1024).decode('ascii')
                    with open('accounts.json', 'r') as f:
                        data = json.load(f)
                    # Store the info of the new server in servers.json
                    with open('accounts.json', 'w') as f:
                        data[username] = {"password":user_password}
                        json.dump(data, f, indent=4)
                    logins.add(client)
                    client.close()
                    continue
                else:
                    client.send('INVALID'.encode('ascii'))
                    client.close()
                    continue
    except Exception as e:
            print('Error Occurred: ', e)
            server.close() 
                
        



receive()