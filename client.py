from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps
from model import NodeInfo
from monitor import Monitor
from time import sleep
from os import environ


HOST = environ.get('HOST', 'localhost')  # Standard loopback interface address (localhost)
PORT = environ.get('PORT', 65432)        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = environ.get('SOCKET_BUFFER_SIZE', 1024) 
CHECK_INTERVAL = environ.get('CHECK_INTERVAL', 10)


def send_node_info(socket: socket, node_info: NodeInfo) -> None:
    socket.sendall(dumps(node_info))


if __name__ == '__main__':
    monitor = Monitor()

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f'Connected to {HOST}:{PORT}')
        monitor.add_callback(lambda x: send_node_info(s, x))
        monitor.add_callback(lambda x: print(f'Sending Node Info:\n{x}'))
        try:
            while True:
                monitor.run()
                sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print('Client stopped')
