import sys
import select
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from common.variables import RESPONSE, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ALERT, DEFAULT_PORT, MAX_CONNECTION
import logging
import logs.server_log_config

logger = logging.getLogger('chatapp.server')


def main():
    try:
        address = sys.argv[sys.argv.index('-a') + 1] if '-a' in sys.argv else ''
    except IndexError:
        logger.critical('Incorrect IP specified during server startup.')
        sys.exit(1)

    try:
        port = int(sys.argv[sys.argv.index('-p') + 1]) if '-p' in sys.argv else DEFAULT_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except ValueError:
        logger.critical('The input number for the port must be in the range from 1024 to 65535.')
        sys.exit(1)
    except IndexError:
        logger.critical('When starting the server, the port was not found in the parameters.')
        sys.exit(1)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(MAX_CONNECTION)
    server_socket.settimeout(1)
    client_sockets = []
    logger.debug('The socket is ready to receive messages')

    while True:
        try:
            client, address = server_socket.accept()
        except OSError as e:
            print(e.errno)
        else:
            client_sockets.append(client)
        finally:
            write, read, err = select.select(client_sockets, client_sockets, [], 0)
            data = ''
            if write:
                for message in write:
                    data = get_message(message)
            if read:
                for message in read:
                    send_message(message, data)


if __name__ == '__main__':
    main()
