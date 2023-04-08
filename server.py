from socket import socket, AF_INET, SOCK_STREAM
from model.model import NodeInfo
from pickle import loads
from threading import Thread
from typing import List, Dict
from os import environ

HOST = environ.get('HOST', '127.0.0.1')  # Standard loopback interface address (localhost)
PORT = environ.get('PORT', 65432)        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = environ.get('SOCKET_BUFFER_SIZE', 1024) 

run: bool = True

last_node_info: Dict[int, NodeInfo] = {}

def handle_connected_client(client_socket: socket):
    global run
    # do not like this, but it works
    with client_socket:
        while run:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            node_info: NodeInfo = loads(data) #TODO save to file
            last_node_info[node_info.hostname] = node_info

threads : List[Thread] = []

def start_server():
    global run
    print('Starting server...')
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while run:
            conn, addr = s.accept()
            print(f'Connected by {addr}')

            thr: Thread = Thread(target=handle_connected_client, args=(conn,))
            threads.append(thr)
            thr.start()

def stop_server():
    global run
    print('Stopping server...')
    run = False
    for thr in threads:
        thr.join()
    print('Server stopped')

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        stop_server()
