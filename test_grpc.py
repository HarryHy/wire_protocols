from server import *
import unittest
from unittest.mock import MagicMock
import chat_pb2
import grpc


class TestChatServer(unittest.TestCase):

    def setUp(self):
        # Initialize the server and context objects for testing
        self.server = ChatService()
        self.context = MagicMock()

    '''def test_sign_up_success(self):
        # Test that a new user can be successfully signed up
        user_id = "testuser"
        password = "testpass"
        request = chat_pb2.UserCredentials(user_id=user_id, password=password)
        response = self.server.SignUp(request, self.context)
        print(response)
        self.assertTrue(response.success)'''  # We commented this out because once we created a test account this will return an error of user already exists! You can delete the test account in json file and uncomment this function and it should work!

    def test_sign_up_already_exists(self):
        # Test that signing up with an existing username returns an error
        user_id = "testuser"
        password = "testpass"
        request = chat_pb2.UserCredentials(user_id=user_id, password=password)
        response = self.server.SignUp(request, self.context)
        self.assertFalse(response.success)
        self.assertEqual(response.error_message, "User already exists")

    def test_sign_in_success(self):
        # Test that a user can successfully sign in
        user_id = "testuser"
        password = "testpass"
        request = chat_pb2.UserCredentials(user_id=user_id, password=password)
        response = self.server.SignIn(request, self.context)
        self.assertTrue(response.success)

    def test_sign_in_failure(self):
        # Test that a user cannot sign in with incorrect credentials
        user_id = "testuser"
        password = "wrongpass"
        request = chat_pb2.UserCredentials(user_id=user_id, password=password)
        response = self.server.SignIn(request, self.context)
        self.assertFalse(response.success)
        self.assertEqual(response.error_message, "Authentication failed")

    def test_SignOut(self):
        # create a mock user and set it as logged in
        user_id = "testuser2"
        password = "123"
        request = chat_pb2.UserCredentials(user_id=user_id, password=password)
        response = self.server.SignIn(request, self.context)
        response = self.server.SignOut(request, self.context)
        print(response)
        self.assertEqual(response.success, True)
        self.assertEqual(self.server.users[user_id].is_logged_in, False)

    def test_list(self):
        # list all users
        query_1 = "*t"
        user_id = "testuser2"
        password = "123"
        request = chat_pb2.UserCredentials(user_id=user_id, password=password)
        self.server.SignIn(request, self.context)
        request = chat_pb2.UserQuery(query=query_1)
        list_response = self.server.ListUsers(request, None)
        empty = ''
        self.assertNotEqual(list_response, empty)

    def test_send_message_to_nonexistent_recipient(self):
        # Create a request with a recipient that does not exist
        user_id = "alice"
        password = "123"
        request = chat_pb2.UserCredentials(user_id=user_id, password=password)
        self.server.SignIn(request, self.context)
        request = chat_pb2.Message(
            from_user_id="alice",
            to_user_id="bob",
            text="Hello",
            password="123"
        )
        # Call the SendMessage function with the request and context objects
        response = self.server.SendMessage(request, self.context)

        # Check that the response indicates an error
        self.assertFalse(response.delivered)
        self.assertEqual(response.error_message, "Recipient not found")

    def test_send_message_success(self):
        user_id = "alice"
        password = "123"
        user_id_2 = "adam"
        request = chat_pb2.UserCredentials(
            user_id=user_id_2, password=password)
        self.server.SignIn(request, self.context)
        request = chat_pb2.UserCredentials(user_id=user_id, password=password)
        self.server.SignIn(request, self.context)
        request = chat_pb2.Message(
            from_user_id="alice",
            to_user_id="adam",
            text="Hello",
            password="123"
        )
        # Call the SendMessage function with the request and context objects
        response = self.server.SendMessage(request, self.context)
        print(response)
        # Check that the response indicates an error
        self.assertTrue(response.delivered)

    def test_send_message_to_offline(self):
        # Create a request with a recipient that does not exist
        user_id = "alice"
        password = "123"
        user_id_2 = "adam"
        request = chat_pb2.UserCredentials(
            user_id=user_id_2, password=password)
        self.server.SignIn(request, self.context)
        self.server.SignOut(request, self.context)
        request = chat_pb2.UserCredentials(user_id=user_id, password=password)
        self.server.SignIn(request, self.context)
        request = chat_pb2.Message(
            from_user_id="alice",
            to_user_id="adam",
            text="Hello",
            password="123")
        response = self.server.SendMessage(request, self.context)
        self.assertFalse(response.delivered)
        self.assertEqual(response.error_message,
                         "User not logged in, message is queued")


if __name__ == '__main__':
    unittest.main()
