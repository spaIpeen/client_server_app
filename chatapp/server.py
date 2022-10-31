import sys
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from common.variables import RESPONSE, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ALERT, DEFAULT_PORT, MAX_CONNECTION
import logging
import logs.server_log_config

logger = logging.getLogger('chatapp.server')


def generate_response(message):
    logger.debug('Generating response')
    logger.info('200/OK')
    if (message.get(ACTION) is not None and message[ACTION] == PRESENCE and message.get(TIME) is not None
            and message.get(USER) is not None and message[USER][ACCOUNT_NAME] == 'Guest'):
        return {
            RESPONSE: 200,
            ALERT: "OK"
        }
    else:
        logger.info('400/BAD REQUEST')
        return {
            RESPONSE: 400,
            ALERT: "BAD REQUEST"
        }


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
    logger.debug('The socket is ready to receive messages')
    while True:
        client, address = server_socket.accept()
        try:
            send_message(client, generate_response(get_message(client)))
            logger.info('The message is received')
            logger.info('The response is sent.')
            client.close()
        except ValueError:
            logger.error('Message type error.')
            client.close()


if __name__ == '__main__':
    main()
