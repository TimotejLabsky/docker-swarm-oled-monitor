from socket import socket, AF_INET, SOCK_STREAM
from model.node_info import NodeInfo
from pickle import loads
from pprint import pprint
from threading import Thread
from typing import List
from time import sleep

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024

run: bool = True
def handle_connected_client(client_socket: socket):
    global run
    # do not like this, but it works
    with client_socket:
        while run:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            node_info: NodeInfo = loads(data)
            # pprint(node_info)
            print(node_info.pid)

threads : List[Thread] = []

def start_server():
    global run
    print('Starting server...')
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.settimeout(5)
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
    start_server()
    sleep(10)
    stop_server()
