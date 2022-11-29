import argparse
import json
import threading
import time
import sys
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from common.variables import ACTION, USER, TIME, ACCOUNT_NAME, PRESENCE, DEFAULT_PORT, MESSAGE,\
    SENDER, DESTINATION, MESSAGE_TEXT, EXIT, DEFAULT_IP_ADDRESS
import logging
import logs.client_log_config

logger = logging.getLogger('chatapp.client')


def create_presence(username='Guest'):
    logger.debug('Generating presence')
    return {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: username
        }
    }


def create_message(sock, username='Guest'):
    to_user = input('Enter recipient: ')
    message = input('Enter your message text: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: username,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    try:
        send_message(sock, message_dict)
    except Exception as e:
        print(e)
        sys.exit(1)


def create_exit_message(username):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: username
    }


def print_help():
    print('Hints:\n\tmessage - send a message.\n\thelp - display hints for commands.\n\texit - exit the program')


def user_interactive(sock, username):
    print_help()
    while True:
        command = input('Enter the command: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Terminating the connection.')
            time.sleep(0.5)
            break
        else:
            print('This command was not found. Type "help" to display the available commands.')


def message_from_server(sock, username):
    while True:
        try:
            message = get_message(sock)
            if (ACTION in message and message[ACTION] == MESSAGE
                    and SENDER in message and DESTINATION in message
                    and MESSAGE_TEXT in message and message[DESTINATION] == username):
                print(f'\nMessage received from user {message[SENDER]}: {message[MESSAGE_TEXT]}')
            else:
                print(f'Message received from user: {message}')
        except (OSError, ConnectionError, ConnectionAbortedError, json.JSONDecodeError):
            print(f'Lost connection to server.')
            break


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        print(f'An attempt was made to start a client with the wrong port number: {server_port}.'
              f'Valid addresses from 1024 to 65535')
        sys.exit(1)

    return server_address, server_port, client_name


def main():
    server_address, server_port, client_name = arg_parser()
    print(f'Console messenger. Client module. Username: {client_name}')
    if not client_name:
        client_name = input('Enter username: ')
    logger.debug(f'The client is launched with parameters: server address: {server_address}, '
                 f'port: {server_port}, username: {client_name}')

    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((server_address, server_port))
        send_message(client_socket, create_presence(client_name))
        answer = get_message(client_socket)
        logger.info(f'A connection to the server has been established. Server response: {answer}')
        logger.info('Successful connection to the server.')
    except json.JSONDecodeError:
        logger.error('Failed to decode received json string.')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.error('Invalid ip or port specified to connect to the server.')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=message_from_server, args=(client_socket, client_name))
        receiver.daemon = True
        receiver.start()
        user_interface = threading.Thread(target=user_interactive, args=(client_socket, client_name))
        user_interface.daemon = True
        user_interface.start()
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
