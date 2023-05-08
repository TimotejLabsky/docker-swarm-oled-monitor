from socket import socket, AF_INET, SOCK_STREAM
from model.model import NodeInfo
from pickle import loads
from threading import Thread
from typing import List, Dict
from os import environ
from logging import Logger, getLogger, basicConfig, Handler, INFO, Formatter
from logging.handlers import RotatingFileHandler

HOST = environ.get('HOST', '0.0.0.0')  # Standard loopback interface address (localhost)
PORT = environ.get('PORT', 65433)        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = environ.get('SOCKET_BUFFER_SIZE', 1024) 

run: bool = True

FORMAT = '%(asctime)s %(levelname)s %(funcName)s %(message)s'
basicConfig(level=INFO, format=FORMAT)
log: Logger = getLogger(__name__)

last_node_info: Dict[int, NodeInfo] = {}

def handle_connected_client(client_socket: socket, log_hander: Handler):
    global run

    log: Logger = getLogger(f"Client: {client_socket.getpeername()}")
    log.setLevel(INFO)
    log.addHandler(log_hander)

    # do not like this, but it works
    with client_socket:
        while run:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                log.warn('Disconnected')
                break
            node_info: NodeInfo = loads(data) #TODO save to file
            log.info(f"{node_info}")
            last_node_info[node_info.hostname] = node_info

threads : List[Thread] = []

def start_server():
    global run
    log.info('Starting server...')

    fh: RotatingFileHandler = RotatingFileHandler('node_info.log', backupCount=3, maxBytes=1024*1024*10)
    fh.setFormatter(Formatter('%(asctime)s %(name)s %(message)s'))

    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        log.info(f'Server started on {HOST}:{PORT}')
        while run:
            conn, addr = s.accept()
            log.info(f'Connected by {addr}')

            thr: Thread = Thread(target=handle_connected_client, args=(conn, fh, ))
            threads.append(thr)
            thr.start()

def stop_server():
    global run
    log.info('Stopping server...')
    run = False
    for thr in threads:
        thr.join()
    log.info('Server stopped')

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        stop_server()
