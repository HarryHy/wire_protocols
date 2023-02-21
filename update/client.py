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
        try:
            response = self.stub.SignUp(chat_pb2.UserCredentials(user_id=user_id, password=password))
            print('Signed up user:', user_id)
            self.user_id = user_id
            self.password = password
            return True
        except Exception as e:
            print(e)
            print("User already exists")
            return False

    def signIn(self):
        user_id = input('Enter user ID: ')
        password = input('Enter password: ')
        try:
            response = self.stub.SignIn(chat_pb2.UserCredentials(user_id=user_id, password=password))
            print('Signed in as:', user_id)
            self.user_id = user_id
            self.password = password
            return True
        except Exception as e:
            print("User not found")
            return False

    def signOut(self):
        if self.user_id:
            response = self.stub.SignOut(chat_pb2.UserCredentials(user_id=self.user_id, password=self.password))
            if not response.success:
                print(response.error_message)
                return
            self.user_id = None
            self.password = None
            print('Signed out')
        else:
            print('Not signed in')

    def listUsers(self):
        try:
            query = input('Enter user ID query (* for all users): ')
            print('All users:')
            for user in self.stub.ListUsers(chat_pb2.UserQuery(query=query)):
                print(user.user_id)
        except Exception as e:
            print("Wrong Query")

    def sendMessage(self):
        if not self.user_id:
            print('Not signed in')
            return
        to_user_id = input('Enter recipient user ID: ')
        text = input('Enter message text: ')
        response = self.stub.SendMessage(chat_pb2.Message(from_user_id=self.user_id, to_user_id=to_user_id, text=text, password=self.password))
        if response.delivered:
            print('Message delivered')
        else:
            print(response.error_message)

    def receiveMessage(self):
        if not self.user_id:
            print('Not signed in')
            return
        print('Messages:')
        for message in self.stub.ReceiveMessage(chat_pb2.MessageQuery(user_id=self.user_id)):
            print(message.text)

    def deleteAccount(self):
        '''
        confirm password before delete (ask user to insert password and id)
        '''
        if not self.user_id:
            print('Not signed in')
            return
        password = input('Confirm your password: ')
        try:
            response = self.stub.DeleteAccount(chat_pb2.UserCredentials(user_id=self.user_id, password=password))
            print('Account deleted')
            self.user_id = None
            self.password = None
        except Exception as e:
            print("Wrong Password")

    def signUpOrSignIn(self):
        while True:
            print('1. Sign up')
            print('2. Sign in')
            choice = input('Enter your choice: ')
            if choice == '1':
                return self.signUp()
            elif choice == '2':
                return self.signIn()
            else:
                print('Invalid choice')

    def run(self):
        while True:
            print('Options:')
            if not self.user_id:
                isHasAccess = self.signUpOrSignIn()
            if isHasAccess:
                print('1. List users')
                print('2. Send message')
                print('3. Receive messages')
                print('4. Delete account')
                print('5. Sign out')
                print('6. Quit')
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
                    self.signOut()
                elif choice == '6':
                    if not self.user_id:
                        print('No user signed in')
                        continue
                    else:
                        try:
                            response = self.stub.SignOut(chat_pb2.UserCredentials(user_id=self.user_id, password=self.password))
                        except Exception as e:
                            print("User not found")
                        print('Signed out')
                        self.user_id = None
                        self.password = None
                        break
                else:
                    print('Invalid choice')

if __name__ == '__main__':
    client = Client()
    client.run()