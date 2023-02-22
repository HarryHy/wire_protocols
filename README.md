# wire_protocols
The wire_protocols is an implementation of a wire protocol that can be used for inter-process communication or data transfer between different devices. 

# Installation & Setup

## Pip
```
pip install pycopy-fnmatch
```

## Manual Installation
- Python 3.7+
- grpcio
- protobuf

# Running the chat box:
To run the chat box, follow these steps:
## Clone the repository to your local machine:
```
git clone https://github.com/XinyuKang/wire_protocols.git
```

## Run server
Start the server by opening a terminal and running:
```
python server.py
```
By default, the server will listen on `127.0.0.1:5555`, you can change the host and port manually inside the `server.py` script

## Run client
Start a client by opening a new terminal and running:
```
python client.py -u user_host -p user_port
```
Replace user_host and user_port with the host and port of the server you want to connect to. Make sure they match the server's host and port, otherwise the connection will fail.

## Login
- If you haven't created an account yet, choose option (2) to create a new account.
- If you already have an account, choose option (1) to sign in. You will be asked to enter your username and password. If the password matches the username, the login will be successful.
- If you want to see a list of existing accounts, choose option (3) to have a full list of usernames, or use wildcard to have a filtered list.

## Choose the user to talk to
- After login, the terminal will ask you to choose a user to talk to. Input the correct username of the person and start your chat
- Once talkto is chosen, the history of the previous messages will be displayed first, and then you can start typing your messages.

## Switch user to talk to
- If you want to switch to another user while chatting, simply type `\switch` and return to the choose talkto page

## Delete your account
- If you want to delete your account, simply type `\delete` during the chat.



## To test the chat box:
To test the chat box, you need to install pytest and mock:
```
pip install pytest
pip install mock
```
After installing the dependencies, run the tests by running the following command in the root directory of the wire_protocols package:
```
pytest
```