import socket
import json
import pickle
import fnmatch
import uuid
import queue
import threading
lock = threading.Lock()

# messages = queue.Queue()


def handle(client):
    while True:
        try:
            operation = client.recv(1024).decode('ascii')
            print("operation is ", operation)

            if operation

        except Exception as e:
            break

def receive(LOGIN_LIMIT = 5, login_times = 0):
    
    while True:

        # connect with the client
        client, addr = server.accept()
        print(f"Connected with {str(addr)}")
        
        operation = client.recv(1024).decode('ascii')
        print("operation is ", operation)
        if operation == "" or operation.startswith("BREAK"):
            break

        elif operation == "STOPCHAT":
            clients[talkto].send(f'{username} left the Chat!'.encode('ascii'))

        elif operation == "LOGIN":
            login_times += 1
            print("logging...")
            if login_times > LOGIN_LIMIT:
                client.send("FAIL".encode('ascii'))
                client.close()

            # check whether username and password match
            # ask the client for the username
            client.send("USERNAME".encode('ascii'))
            # print("already sent USERNAME")
            username = client.recv(1024).decode('ascii')
            # print("username is ", username)
            client.send('PASSWORD'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            # print("password is ", password)
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
                # global user   # current user
                # user = username
                clients[username] = client
                logins.add(username)
                #continue
            #TODO
        elif operation.startswith("SIGNUP"):
            # check whether the username already exists
            os = operation.split(" ")
            if len(os) == 1:
                break
            username = os[1]
            with open('accounts.json') as f:
                data = json.load(f)
            if username in data:
                client.send('DUPNAME'.encode('ascii'))
            else:
                client.send('NONDUPNAME'.encode('ascii'))
                password = client.recv(1024).decode('ascii')
                # generate a unique uuid for the new account
                id = uuid.uuid1()
                # store the new created account into the json file
                with open("accounts.json", "w") as f:
                    data[username] = {"password": password, "id": uuid}
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
        elif operation.startswith("TALKTO"):
            talkto = operation.split(" ")[1]
            # check if the talkto username is valid
            with open('accounts.json') as f:
                data = json.load(f)
            if talkto in data:
                client.send("VALTALKTO".encode('ascii'))
            else:
                lists = pickle.dumps(list(data.keys()))
                client.send(lists)
        elif operation == "STARTHIST":
            # send the queued messages from talkto to user
            lock.acquire()
            with open("histories.json", "r") as f:
                data = json.load(f)
                # from talkto to user
                messages = data[talkto][username]
                tosend = pickle.dumps(messages)
                client.send(tosend)
                # after send all the queued messages, clear the history
                data[talkto][username] = []
            with open("histories.json", 'w') as f:
                json.dump(data, f, indent=4)
            lock.release()

        # elif operation == "STARTCHAT":
        #     # check if the person trying to talkto is online
        #     # if online, start chat
        #     # if offline, queue the user's messages
        #     if talkto in logins:
        #         client.send("CHATNOW".encode('ascii'))
        #     else:
        #         client.send("CHATLATER".encode('ascii'))
                

        # elif operation.startswith("NOW"):
        #     # forward the message to the talkto user
        #     message = operation[4:]
        #     clients[talkto].send(message.encode('ascii'))

        # elif operation.startswith("LATER"):
        #     # queue the message
        #     message = operation[6:]
        #     lock.acquire()
        #     with open("histories.json", "r+") as f:
        #         data = json.load(f)
        #         # from user to talkto
        #         data[user][talkto].append(message)
        #     lock.release()

        else:
            if talkto in logins:
                clients[talkto].send(operation.encode('ascii'))
            else:
                print("the user is not logged in")
                lock.acquire()
                with open("histories.json", "r") as f:
                    data = json.load(f)
                    # from user to talkto
                    print("now writing to json")
                    old_list = data[username][talkto]
                    old_list.append(operation.split(":")[1])
                    data[username][talkto] = old_list
                with open("histories.json", 'w') as f:
                    json.dump(data, f, indent=4)
                lock.release()
        
     

    print("Client side ends connection")
    print(f'{username} left the Chat!')
    if "talkto" in globals():
        clients[talkto].send(f'{username} left the Chat!'.encode('ascii'))
    clients.pop(username)
    logins.remove(username)
    client.close()
        
                    

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 5555
    # keep a set of already logged in users
    logins = set()
    # keep a number of logged in times, exceeding this limit will cause break of the connection
    LOGIN_LIMIT = 5
    login_times = 0
    talkto = ""
    clients = dict()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print('Listening...')
    try:
        receive(LOGIN_LIMIT, login_times )
    except Exception as e:
        print('Error Occurred: ', e)
        server.close() 