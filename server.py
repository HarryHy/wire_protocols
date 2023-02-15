import socket
import json
import pickle
import fnmatch
import uuid
import queue
import threading
import os
import os.path
import sys

lock = threading.Lock()
messages = queue.Queue()
users = []
global talkto


def receive(client, addr, LOGIN_LIMIT = 5, login_times = 0):
    # connect with the client
    # client, addr = server.accept()
    print(f"Connected with {str(addr)}")
    while True:
        
        operation = client.recv(1024).decode('ascii')
        print("operation is ", operation)
        if operation == "LOGIN":
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
                clients[username] = client
                logins.add(username)
                print("add " + username + " to logins")
                global user
                user = username
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
            global talkto
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
            with open("histories.json", "r+") as f:
                data = json.load(f)
                # from talkto to user
                print("1")
                print(talkto, data.keys())
                if talkto in data.keys():
                    print("2")
                    print(user, data[talkto].keys())
                    if user in data[talkto].keys():
                        # maybe data[talkto][user] will return a key not find error
                        messages = data[talkto][user]
                        if not len(messages)==0:
                            client.send("NOTEMPTY".encode('ascii'))
                        #
                            tosend = pickle.dumps(messages)
                            client.send(tosend)
                        
                        # after send all the queued messages, clear the history
                            print("------clear the message--------")
                            #data[talkto][user] = []lock.acquire()
                            lock.acquire()
                            with open("histories.json", "r") as f:
                                data = json.load(f)
                                data[talkto][user] = []
                            with open("histories.json", 'w') as f:
                                json.dump(data, f, indent=4)
                            lock.release()
                            print("------finish clean--------")
                        
                        else:
                            client.send("EMPTY".encode('ascii'))

        elif operation == "STARTCHAT":
            # check if the person trying to talkto is online
            # if online, start chat
            # if offline, queue the user's messages
            '''
            if talkto in logins:
                client.send("CHATNOW".encode('ascii'))
            else:
                client.send("CHATLATER".encode('ascii'))
            '''
            message_receiver(client, talkto, user)
            #if the user want to start over, the chattiing part is wrapped in the receive.
            break

        elif operation.startswith("BREAK"):
            if server:
                server.close()
            break
        else:
            print("encounter error")
            if server:
                server.close()
            break

def message_receiver(client, talkto, user):
    # A function handling the chatting part
    print("in the message receiver")
    print("talk to is ", talkto, " user is ", user)
    try:
        while True:
            if talkto in logins:
                client.send("CHATNOW".encode('ascii'))
                recv_message = client.recv(1024).decode('ascii')
                user_talk_to = recv_message.split("~")[1]
                user_itself = recv_message.split("~")[2]
                user_message = recv_message.split("~")[3]
                if user_message == "\exit":
                    #user log out 
                    clients.pop(user_itself)
                    logins.remove(user_itself)
                    if client:
                        client.close()
                    break
                # how to send to talkto ?
                #分发给use
                # sender recver message 
                #clients[user_talk_to].send((user_itself + ": "+user_message).encode('ascii')) 
                clients[user_talk_to].send(("CHATNOW" + user_itself + " : "+user_message).encode('ascii')) 
            else:
                client.send("CHATLATER".encode('ascii'))
                recv_message = client.recv(1024).decode('ascii')
                user_talk_to = recv_message.split("~")[1]
                user_itself = recv_message.split("~")[2]
                user_message = recv_message.split("~")[3]
                if user_message == "\exit":
                    #user log out 
                    clients.pop(user_itself)
                    logins.remove(user_itself)
                    if client:
                        client.close()
                    break


                #write to the json file 
                # 这部分不知道 怎么写到 json file 里面 
                #收到消息
                #分发给 json file
                print("the user is not logged in")
                lock.acquire()
                with open("histories.json", "r") as f:
                    data = json.load(f)
                    # from user to talkto
                    print("now writing to json")
                    old_list = data[user_itself][user_talk_to]
                    old_list.append(user_message)
                    data[user_itself][user_talk_to] = old_list
                with open("histories.json", 'w') as f:
                    json.dump(data, f, indent=4)
                lock.release()

    except:
        #This user try to logout or encounter connection error
        clients.pop(user)
        logins.remove(user)
        if client:
            client.close()

    return
                    

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 5555
    # keep a set of already logged in users
    logins = set()
    # keep a number of logged in times, exceeding this limit will cause break of the connection
    LOGIN_LIMIT = 5

    login_times = 0

    talkto = ''
    clients = {} 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    os.chdir(sys.path[0])
    server.bind((host, port))
    server.listen(10)
    print('Listening...')
    try:
        while True:
            client, addr = server.accept()
            #print(f"Connected with {str(addr)}")    
            t = threading.Thread(target=receive, args=(client, addr))
            t.start()
            # t.join()
            #receive(client, addr)
        server.close()     
    except Exception as e:
        print('Error Occurred: ', e)
        print("stop the thread")
        t.join()
        print("stop the server")
        server.close()
