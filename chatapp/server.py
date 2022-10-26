import json
import sys
from socket import socket, AF_INET, SOCK_STREAM
from chatapp.common.utils import send_message, get_message
from chatapp.common.variables import RESPONSE, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ALERT, DEFAULT_PORT


def generate_response(message):
    if (message.get(ACTION) is not None and message[ACTION] == PRESENCE and message.get(TIME) is not None
            and message.get(USER) is not None and message[USER][ACCOUNT_NAME] == 'Guest'):
        return {
            RESPONSE: 200,
            ALERT: "OK"
        }
    else:
        return {
            RESPONSE: 400,
            ALERT: "BAD REQUEST"
        }


def main():
    try:
        port = int(sys.argv[sys.argv.index('-p') + 1]) if '-p' in sys.argv else DEFAULT_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        print("<script's name> -a <address> -p <port>")
        sys.exit(1)
    except ValueError:
        print('1024 < port < 65535')
        sys.exit(1)

    try:
        address = sys.argv[sys.argv.index('-a') + 1] if '-a' in sys.argv else ''
    except IndexError:
        print("<script's name> -a <address> -p <port>")
        sys.exit(1)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(5)

    while True:
        client, address = server_socket.accept()
        try:
            send_message(client, generate_response(get_message(client)))
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Error message')
            client.close()


if __name__ == '__main__':
    main()
