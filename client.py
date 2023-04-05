from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from model.node_info import NodeInfo
from monitor import Monitor
from time import sleep


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024
CHECK_INTERVAL = 1


def send_node_info(socket: socket, node_info: NodeInfo) -> None:
    socket.sendall(dumps(node_info))



def start_client(socket: socket, monitor: Monitor):
    socket.connect((HOST, PORT))

    monitor.add_callback(lambda x: send_node_info(s, x))
    monitor.add_callback(lambda x: print(f'Sending Node Info\n{x}'))

    monitor.start()

if __name__ == '__main__':
    monitor = Monitor(CHECK_INTERVAL)

    with socket(AF_INET, SOCK_STREAM) as s:
        try:
            start_client(s , monitor)
            while True:
                sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            monitor.stop()
            monitor.join()
            print('Client stopped')
