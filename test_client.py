import unittest
import socket
from unittest import mock
from unittest.mock import MagicMock, patch
from unittest.mock import Mock
from c2 import ChatClient


class TestChatClient(unittest.TestCase):
    # def setUp(self):
    #     self.client = ChatClient("localhost", 56789)

    def test_init(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 56789)
            self.assertEqual(client.server_host, "localhost")
            self.assertEqual(client.server_port, 56789)
            self.assertEqual(client.client, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            client.client.connect.assert_called_once_with(("localhost", 56789))

    def test_send_message(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 12345)
            client.username = "alice"
            client.send("hello")
            client.client.send.assert_called_once_with("hello")

    def test_close(self):
        with mock.patch('socket.socket'):
            client = ChatClient("localhost", 12345)
            client.username = "alice"
            client.close()
            client.client.close.assert_called_once()
    
    def test_login_with_valid_credentials(self):
        # Arrange
        with mock.patch('socket.socket'):
            client = ChatClient('localhost', 8000)
            client.client.recv = Mock(side_effect=[
                'USERNAME'.encode('ascii'),
                'PASSWORD'.encode('ascii'),
                'OK'.encode('ascii')
            ])
            
            # Act
            result = client.login('testuser', 'testpassword')
            
            # Assert
            self.assertEqual(result, 0)
            self.assertEqual(client.username, 'testuser')

    def test_login_with_invalid_username(self):
        # Arrange
        with mock.patch('socket.socket'):
            client = ChatClient('localhost', 8000)
            client.client.recv = Mock(side_effect=[
                'USERNAME'.encode('ascii'),
                'PASSWORD'.encode('ascii'),
                'NOUSER'.encode('ascii')
            ])
            
            # Act
            result = client.login('testuser', 'testpassword')
            
            # Assert
            self.assertEqual(result, 1)
            self.assertIsNone(client.username)

    def test_login_with_invalid_password(self):
        # Arrange
        with mock.patch('socket.socket'):
            client = ChatClient('localhost', 8000)
            client.client.recv = Mock(side_effect=[
                'USERNAME'.encode('ascii'),
                'PASSWORD'.encode('ascii'),
                'REJECT'.encode('ascii')
            ])
            
            # Act
            result = client.login('testuser', 'testpassword')
            
            # Assert
            self.assertEqual(result, 1)
            self.assertIsNone(client.username)
        

if __name__ == "__main__":
    #mock_socket = mock.Mock()
    test = TestChatClient()
    test.test_init()
    test.test_send_message()
    test.test_close()
    test.test_login_with_valid_credentials()
    test.test_login_with_invalid_username()
    test.test_login_with_invalid_password()
