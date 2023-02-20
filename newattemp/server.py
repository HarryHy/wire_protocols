import grpc
from concurrent import futures
import time

import chat_pb2
import chat_pb2_grpc

class User:
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.users = {}
        self.message_queue = {}

    def SignUp(self, request, context):
        if request.user_id in self.users:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('User already exists')
            return chat_pb2.User()
        user = User(request.user_id, request.password)
        self.users[user.user_id] = user
        return chat_pb2.User(user_id=user.user_id)

    def ListUsers(self, request, context):
        for user in self.users.values():
            if request.query == '*' or request.query in user.user_id:
                yield chat_pb2.User(user_id=user.user_id)

    def SendMessage(self, request, context):
        print("send message log")
        print(request.from_user_id)
        print(request.to_user_id)
        print(request.text)
        if request.to_user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Recipient not found')
            return chat_pb2.SendMessageResponse(delivered=False)
        if request.from_user_id not in self.users or self.users[request.from_user_id].password != request.password:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Authentication failed')
            return chat_pb2.SendMessageResponse(delivered=False)
        message = chat_pb2.Message(
            from_user_id=request.from_user_id,
            to_user_id=request.to_user_id,
            text=f"{request.from_user_id}: "+request.text,
        )
        if request.to_user_id in self.message_queue:
            self.message_queue[request.to_user_id].append(message)
            return chat_pb2.SendMessageResponse(delivered=False)
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

    def DeleteAccount(self, request, context):
        if request.user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return chat_pb2.DeleteAccountResponse(success=False, error_message='User not found')
        if request.user_id in self.message_queue:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('User has undelivered messages')
            return chat_pb2.DeleteAccountResponse(success=False, error_message='User has undelivered messages')
        if self.users[request.user_id].password != request.password:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Authentication failed')
            return chat_pb2.DeleteAccountResponse(success=False, error_message='Authentication failed')
        del self.users[request.user_id]
        return chat_pb2.DeleteAccountResponse(success=True)
if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
