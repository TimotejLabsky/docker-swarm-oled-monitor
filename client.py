from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from model.node_info import NodeInfo
from monitor import Monitor
from time import sleep


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024


def send_node_info(socket: socket, node_info: NodeInfo) -> None:
    s.sendall(dumps(node_info))

m = Monitor()


with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    m.add_callback(lambda x: send_node_info(s, x))
    m.start()

    sleep(100)
    m.stop()