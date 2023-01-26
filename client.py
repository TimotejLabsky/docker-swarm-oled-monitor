from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from model.node_info import NodeInfo
from monitor import get_node_info

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024

with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Send NodeInfo to servier and reci
    node_info = get_node_info()
    s.sendall(dumps(node_info))