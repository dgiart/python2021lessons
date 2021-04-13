import socket
from select import select
import os

to_monitor = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr}')
    to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)
    # print(f'request: {request}')
    if request:
        response = f'Hop-Hop {request}'.encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:

        print(f'to_monitor before select: {to_monitor}')
        print(f'LENGTH to_monitor before select: {len(to_monitor)}')
        ready_to_read, _, _ = select(to_monitor, [], [])
        print(f'to_monitor AFTER select: {to_monitor}')
        print(f'ready_to_read: {ready_to_read}')
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
    # print(os.getcwd())
    # print(os.listdir())
    # with open ('select1.py') as f:
    #     print(select([f], [], []))
    # accept_connection(server_socket)
