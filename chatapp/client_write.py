import sys
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from common.variables import DEFAULT_PORT
import logging
import logs.client_log_config

logger = logging.getLogger('chatapp.client')


def generate_presence():
    message = input('What you say?')
    logger.debug('Generating presence')
    return message


def main():
    try:
        address = sys.argv[1]
    except IndexError:
        logger.critical('You need to specify the IP of the server.')
        sys.exit(1)

    try:
        port = int(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        logger.critical('You need to specify the port of the server.')
        sys.exit(1)
    except ValueError:
        logger.critical('The input number for the port must be in the range from 1024 to 65535.')
        sys.exit(1)

    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((address, port))
        logger.info('Successful connection to the server.')
        while True:
            send_message(client_socket, generate_presence())
            logger.info('The message is sent')
    except ConnectionRefusedError:
        logger.error('Invalid ip or port specified to connect to the server.')
        sys.exit(1)


if __name__ == '__main__':
    main()
