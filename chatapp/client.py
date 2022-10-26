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


def main():
    try:
        address = sys.argv[1]
    except IndexError:
        print('Необходимо указать ip сервера')

    try:
        port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        print("<script's name> <address> <port>")
        sys.exit(1)
    except ValueError:
        print('1024 < port < 65535')
        sys.exit(1)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((address, port))
    send_message(client_socket, generate_presence())
    get_message(client_socket)
    client_socket.close()


if __name__ == '__main__':
    main()
