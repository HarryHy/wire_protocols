import threading
import socket
import json
import pickle
import fnmatch



def receive(LOGIN_LIMIT = 5, login_times = 0):
    # connect with the client
    client, addr = server.accept()
    print(f"Connected with {str(addr)}")
    while True:
        
        operation = client.recv(1024).decode('ascii')
        print("operation is ", operation)
        if operation == "LOGIN":
            login_times += 1
            print("logging")
            if login_times > LOGIN_LIMIT:
                client.send("FAIL".encode('ascii'))
                client.close()

            # check whether username and password match
            # ask the client for the username
            client.send("USERNAME".encode('ascii'))
            print("already sent USERNAME")
            username = client.recv(1024).decode('ascii')
            print("username is ", username)
            client.send('PASSWORD'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            print("password is ", password)
            # check if password matches with user name
            with open('accounts.json') as f:
                data = json.load(f)
            if username not in data.keys():
                print("No such user")
                client.send("NOUSER".encode('ascii'))
            elif password != data[username]["password"]:
                print("Login rejected!")
                client.send("REJECT".encode('ascii'))
                #continue # returns the control to the beginning of the while loop
            else:
                print("Successfully logged in! as ", username)
                client.send("ACCEPT".encode('ascii'))
                logins.add(username)
                #continue
            #TODO
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
        elif operation.startswith("LIST"):
            pattern = operation.split(" ")[1]
            with open('accounts.json') as f:
                    data = json.load(f)
            if pattern == "ALL":
                keys = list(data.keys())
            else:
                keys = []
                for k in list(data.keys()):
                    if fnmatch.fnmatch(k, pattern):
                        keys.append(k)
            if len(keys) == 0:
                client.send("NOMATCHED".encode('ascii'))
            else:
                client.send("MATCHED".encode('ascii'))
                next_line = client.recv(1024).decode('ascii')
                if next_line == "SENDMATCHED":
                    lists = pickle.dumps(keys)
                    client.send(lists)   
        
        elif operation.startswith("BREAK"):
            break
        
                    

if __name__ == '__main__':
    host = "127.0.0.1"
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
    try:
        receive(LOGIN_LIMIT, login_times )
    except Exception as e:
        print('Error Occurred: ', e)
        server.close() 