import grpc
import chat_pb2
import chat_pb2_grpc

class Client:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)
        self.user_id = None
        self.password = None

    def signUp(self):
        user_id = input('Enter user ID: ')
        password = input('Enter password: ')
        response = self.stub.SignUp(chat_pb2.UserCredentials(user_id=user_id, password=password))
        print('Signed up user:', response.user_id)
        self.user_id = user_id
        self.password = password

    def listUsers(self):
        query = input('Enter user ID query (* for all users): ')
        print('All users:')
        for user in self.stub.ListUsers(chat_pb2.UserQuery(query=query)):
            print(user.user_id)

    def sendMessage(self):
        to_user_id = input('Enter recipient user ID: ')
        text = input('Enter message text: ')
        response = self.stub.SendMessage(chat_pb2.Message(from_user_id=self.user_id, to_user_id=to_user_id, text=text,password=self.password))
        if response.delivered:
            print('Message delivered')
        else:
            print('Message queued for later delivery')

    def receiveMessage(self):
        print('Messages:')
        for message in self.stub.ReceiveMessage(chat_pb2.MessageQuery(user_id=self.user_id)):
            print(message.text)

    def deleteAccount(self):
        response = self.stub.DeleteAccount(chat_pb2.UserCredentials(user_id=self.user_id, password=self.password))
        if response.success:
            print('Account deleted')
            self.user_id = None
            self.password = None
        else:
            print('Failed to delete account:', response.error_message)

    def run(self):
        while True:
            if not self.user_id:
                self.signUp()
            print('Options:')
            print('1. List users')
            print('2. Send message')
            print('3. Receive messages')
            print('4. Delete account')
            print('5. Quit')
            choice = input('Enter your choice: ')
            if choice == '1':
                self.listUsers()
            elif choice == '2':
                self.sendMessage()
            elif choice == '3':
                self.receiveMessage()
            elif choice == '4':
                self.deleteAccount()
            elif choice == '5':
                break
            else:
                print('Invalid choice')

if __name__ == '__main__':
    client = Client()
    client.run()