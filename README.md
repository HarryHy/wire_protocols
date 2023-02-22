# GRPC 

## Installation 

We used Python 3.9+ to develop this program. Please use pip to install all the dependencies. Create a virtual environment, then run:

```
pip install -r requirements.txt
```
## Deployment 

Start the server with 
```
python3/python server.py
```
Start clients with 
```
python3/python client.py
```
You can start multiple instances of client (<=10). 

### Sign up/Sign in
For the first time users, choose 1 for sign up, enter desired username and password. 
If your username is not unique, the program will print an error message. And you will automically log in after succuessful registration. 
For returning users, choose 2 for sign in and enter username and password. If the username is not existent or password is not correct, the system will print an error message.  

### List
After log in, you will be given a set of options. Choose 1 to list users. Use * to list all users or you can use * as a wildcard such as a* or *a to list users that start with a or end with a. 

### Send Message
You can choose 2 to send message to recipient. If the recipient is not found in the system, it will print out an error message. If the recipient is not logged in at this moment, the program will queue this message and deliver it when the recipient logs in and requests it. 

## Receive Message
You can choose 3 to receive message sent to you. 

### Delete Account 
You can choose 4 to delete your account. If you don't have unread message, the program will propmt you to enter password, and then you can delete your account. If you enter your password wrong, the system will print an error message. If you have unread queued message, the system will print them all and you can proceed to delete your account. 

### Sign Out/Exit
You can choose 5 to sign out or 6 to exit the program. 

### Note 
Sometimes when you close the server and want to restart the server and client. The client will raise an error of failed to connect to all address. 
You can solve this connection issue by close VScode or any IDE you use and start the server and client again. 

## GRPC vs Naive Implementation
GRPC buffer size: Max 4MB 

Areas to cover:
- Packet size
- Code simplicity
- Focus on designing the most optimized wire protocol possible
    - Design experience with sending strings over the wire protocol



