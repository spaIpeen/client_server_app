import time
import sys
from socket import socket, AF_INET, SOCK_STREAM
from chatapp.common.utils import send_message, get_message
from chatapp.common.variables import ACTION, USER, TIME, ACCOUNT_NAME, PRESENCE, DEFAULT_IP_ADDRESS, DEFAULT_PORT


def generate_presence(username='Guest'):
    return {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: username
        }
    }


def main(address=DEFAULT_IP_ADDRESS, port=DEFAULT_PORT):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((address, port))
    send_message(client_socket, generate_presence())
    get_message(client_socket)
    client_socket.close()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        client_port = sys.argv[2] if sys.argv[2].isdigit() else DEFAULT_PORT
        main(sys.argv[1], int(client_port))
    elif len(sys.argv) == 1:
        main()
    else:
        main(sys.argv[1])
