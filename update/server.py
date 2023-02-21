import grpc
from concurrent import futures
import time
import json

import chat_pb2
import chat_pb2_grpc

class User:
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.is_logged_in = False
        self.queued_messages = []
    def to_dict(self):
        return {
            "user_id":self.user_id,
            "password":self.password,
            "is_logged_in":self.is_logged_in,
            "queued_messages":[ChatService.messgae_to_dict(msg) for msg in self.queued_messages]
        }
class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.users:dict[str,User] = {}
        self.message_queue = {}
        self.load_users()

    # Utils
    def load_users(self):
        try:
            with open('users.json', 'r') as f:
                users_data = json.load(f)
                for user_data in users_data:
                    user = User(user_data['user_id'], user_data['password'])
                    user.is_logged_in = user_data['is_logged_in']
                    user.queued_messages = [ChatService.dict_to_Message(msg) for msg in user_data['queued_messages']]
                    self.users[user.user_id] = user
        except FileNotFoundError:
            pass

    def save_users(self):
        with open('users.json', 'w') as f:
            users_data = []
            for user in self.users.values():
                users_data.append(user.to_dict())
            json.dump(users_data, f)

    def get_logged_in_users(self):
        logged_in_users = []
        for user in self.users.values():
            if user.is_logged_in:
                logged_in_users.append(user.user_id)
        return logged_in_users
    @staticmethod
    def messgae_to_dict(msg:chat_pb2.Message):
        return {
            "from_user_id":msg.from_user_id,
            "to_user_id":msg.to_user_id,
            "text":msg.text,
            "password":msg.password
        }
    
    @staticmethod
    def dict_to_Message(msg:dict):
        return chat_pb2.Message(
            from_user_id=msg['from_user_id'],
            to_user_id=msg['to_user_id'],
            text=msg['text'],
            password=msg['password']
        )
    
    # Main Methods
    def SignUp(self, request, context):
        if request.user_id in self.users:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('User already exists')
            return chat_pb2.SignUpResponse(success=False,error_message="User already exists")
        user = User(request.user_id, request.password)
        self.users[user.user_id] = user
        self.users[user.user_id].is_logged_in = True
        self.save_users()
        return chat_pb2.SignUpResponse(success=True)

    def ListUsers(self, request, context):
        if request.query == "*":
            for user in self.users.values():
                yield chat_pb2.User(user_id=user.user_id)
        elif request.query[0] == "*":
            for user in self.users.values():
                if user.user_id.endswith(request.query[1:]):
                    yield chat_pb2.User(user_id=user.user_id)
        elif request.query[-1] == "*":
            for user in self.users.values():
                if user.user_id.startswith(request.query[:-1]):
                    yield chat_pb2.User(user_id=user.user_id)
        else:
            for user in self.users.values():
                if request.query in user.user_id:
                    yield chat_pb2.User(user_id=user.user_id)

    def SignIn(self, request, context):
        if request.user_id not in self.users or self.users[request.user_id].password != request.password:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Authentication failed')
            return chat_pb2.SignInResponse(success=False,error_message="Authentication failed")
        self.users[request.user_id].is_logged_in = True
        self.save_users()
        respo =  chat_pb2.SignInResponse(success=True)
        print(respo)
        return respo

    def SignOut(self, request, context):
        if request.user_id not in self.users or not self.users[request.user_id].is_logged_in:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Not logged in')
            return chat_pb2.SignOutResponse(error_message='Not logged in',success=False)
        self.users[request.user_id].is_logged_in = False
        self.save_users()
        self.load_users()
        return chat_pb2.SignOutResponse(success=True)

    def SendMessage(self, request, context):
            if request.to_user_id not in self.users:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Recipient not found')
                return chat_pb2.SendMessageResponse(delivered=False,error_message="Recipient not found")

            if request.from_user_id not in self.users or self.users[request.from_user_id].password != request.password:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details('Authentication failed')
                return chat_pb2.SendMessageResponse(delivered=False,error_message="Authentication failed")

            message = chat_pb2.Message(
                from_user_id=request.from_user_id,
                to_user_id=request.to_user_id,
                text=f"{request.from_user_id}: "+request.text,
                password=request.password
            )

            # Check if the recipient is logged in
            recipient_logged_in = request.to_user_id in self.get_logged_in_users()

            # If the recipient is not logged in, queue the message
            if not recipient_logged_in:
                message.text = "--> Queued message: "+message.text
                self.users[request.to_user_id].queued_messages.append(message)
                return chat_pb2.SendMessageResponse(delivered=False, error_message="User not logged in, message is queued")

            # If the recipient is logged in, deliver the message and remove it from the queue
            if request.to_user_id in self.message_queue:
                self.message_queue[request.to_user_id].append(message)
            else:
                self.message_queue[request.to_user_id] = [message]
            return chat_pb2.SendMessageResponse(delivered=True)
            
            

    def ReceiveMessage(self, request, context):
        if request.user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return
        if request.user_id in self.message_queue:
            for message in self.message_queue[request.user_id]:
                yield message
            del self.message_queue[request.user_id]
        # check queued messages
        if request.user_id in self.users and len(self.users[request.user_id].queued_messages) > 0:
            for message in self.users[request.user_id].queued_messages:
                yield message
            self.users[request.user_id].queued_messages = []
        else:
            yield chat_pb2.Message(text="No new messages.")


    # implement this rpc DeleteAccount(UserCredentials) returns (DeleteAccountResponse) {}
    def DeleteAccount(self, request, context):
        if (request.user_id not in self.users) or (self.users[request.user_id].password != request.password):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Authentication failed')
            return chat_pb2.DeleteAccountResponse(success=False,error_message="Authentication failed")
        self.users.pop(request.user_id)
        self.save_users()
        return chat_pb2.DeleteAccountResponse(success=True)


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server Started.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
