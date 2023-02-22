import subprocess
import socket
import time

# def start_server():
#     # Start the server script in a subprocess
#     server_process = subprocess.Popen(['python', 'server.py'])
#     # Wait for the server to start up
#     time.sleep(1)
#     return server_process

# def start_client():
#     # Start the client script in a subprocess
#     client_process = subprocess.Popen(['python', 'client.py', '-u', '127.0.0.1', '-p', '5555'])
#     # Wait for the client to start up
#     time.sleep(1)
#     return client_process

# def stop_server(server_process):
#     # Stop the server subprocess
#     server_process.terminate()
#     server_process.wait()

# def stop_client(client_process):
#     # Stop the client subprocess
#     client_process.terminate()
#     client_process.wait()

def test_wire_protocol():
    # Start the server and client subprocesses
    # server_process = start_server()
    # client_process = start_client()

    # Connect to the server
    # Receive the test message on the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen(1)
    server_conn, server_addr = server_socket.accept()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    # Send a test message from the client to the server
    client_socket.send(b'TEST MESSAGE')

    
    
#    # Check that the received message matches the sent message
#     message = server_conn.recv(1024)
#     assert message == b'TEST MESSAGE' 

    # # Stop the server and client subprocesses
    # stop_server(server_process)
    # stop_client(client_process)
