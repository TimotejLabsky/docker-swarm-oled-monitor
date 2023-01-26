from socket import socket, AF_INET, SOCK_STREAM
from model.node_info import NodeInfo
from pickle import loads
from pprint import pprint

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            node_info: NodeInfo = loads(data)
            pprint(node_info)