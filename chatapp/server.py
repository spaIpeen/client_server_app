import json
import sys
from socket import socket, AF_INET, SOCK_STREAM
from chatapp.common.utils import send_message, get_message
from chatapp.common.variables import RESPONSE, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ALERT, DEFAULT_PORT

ok = {
        RESPONSE: 200,
        ALERT: "OK"
    }

bad_request = {
        RESPONSE: 400,
        ALERT: "bad request"
    }


def generate_response(message):
    if (message[ACTION] == PRESENCE and message.get(TIME) is not None
            and message.get(USER) is not None and message[USER][ACCOUNT_NAME] == 'Guest'):
        return json.dumps(ok)
    else:
        return json.dumps(bad_request)


def main(address='', port=DEFAULT_PORT):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(5)

    while True:
        client, address = server_socket.accept()
        send_message(client, generate_response(get_message(client)))
        client.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        address_param = sys.argv[sys.argv.index('-a') + 1] if '-a' in sys.argv else ''
        port_param = int(sys.argv[sys.argv.index('-p') + 1]) if '-p' in sys.argv else DEFAULT_PORT
        main(address_param, port_param)
