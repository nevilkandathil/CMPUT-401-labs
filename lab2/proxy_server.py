import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

'''
Accepts requests and relays them to a particular to a target.
When target send a requests it receives and send back to the 
person who made the initial request.
'''

def send_request(host, port, request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # sending data to google
        client_socket.connect((host, port))
        client_socket.send(request_data)
        client_socket.shutdown(socket.SHUT_WR)
        
        # getting response from google
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data

        while len(data) > 0:
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        
        return result

def handle_conn(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        request = b''

        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data
        
        response = send_request("www.google.com", 80, request)
        conn.sendall(response)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
    
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)

        conn, addr = server_socket.accept()
        handle_conn(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
    
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_conn, args=(conn, addr))
            thread.run()

start_threaded_server()

# start_server()