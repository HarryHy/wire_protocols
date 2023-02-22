import pytest
from unittest.mock import patch, Mock
from client import *

def test_login():
    with patch('socket.socket') as mock_socket:
        # Create a mock socket object
        mock_client = Mock()
        mock_socket.return_value = mock_client

        # Call the login function
        login()

        # Assert that the correct message was sent to the server
        mock_client.send.assert_called_once_with('LOGIN'.encode('ascii'))

        # Assert that the username and password were entered correctly
        # assert username == "example"
        # assert password == "123"

# def test_signup():
#     with patch('socket.socket') as mock_socket:
#         # Create a mock socket object
#         mock_client = Mock()
#         mock_socket.return_value = mock_client

#         # Set the response from the server
#         mock_client.recv.return_value.decode.return_value = "NONDUPNAME"

#         # Call the signup function
#         signup()

#         # Assert that the correct message was sent to the server
#         mock_client.send.assert_called_once_with('SIGNUP example'.encode('ascii'))

#         # Assert that the username and password were entered correctly
#         # assert username == "example"
#         # assert password == "test"

def test_listAccounts():
    with patch('socket.socket') as mock_socket:
        # Create a mock socket object
        mock_client = Mock()
        mock_socket.return_value = mock_client

        # Set the response from the server
        mock_client.recv.return_value.decode.return_value = "MATCHED"
        mock_client.recv.return_value = pickle.dumps(["account1", "account2"])

        # Call the listAccounts function
        listAccounts()

        # Assert that the correct message was sent to the server
        mock_client.send.assert_called_once_with('LIST ALL'.encode('ascii'))

        # Assert that the output was printed correctly
        # assert "account1" in capsys.readouterr().out
        # assert "account2" in capsys.readouterr().out
