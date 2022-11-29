import sys
import select
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, DEFAULT_PORT, MAX_CONNECTION, \
    SENDER, RESPONSE_400, ERROR, EXIT, MESSAGE_TEXT, MESSAGE, DESTINATION, RESPONSE_200
import logging
import logs.server_log_config

logger = logging.getLogger('chatapp.server')


def process_client_message(message, messages_list, client, clients, names):
    logger.info(f'Parsing a message from a client : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'The username is already taken.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
            and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    else:
        response = RESPONSE_400
        response[ERROR] = 'The request is invalid.'
        send_message(client, response)
        return


def process_message(message, names, listen_socks):
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        print(f'Sent message to user {message[DESTINATION]} from user {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        print(f'User {message[DESTINATION]} not registered on the server sending message is not possible.')


def generate_response(message):
    logger.debug('Generating response')
    if (message.get(ACTION) is not None and message.get(TIME) is not None
            and message.get(SENDER) is not None):
        logger.info('200/OK')
        return RESPONSE_200
    else:
        logger.info('400/BAD REQUEST')
        return RESPONSE_400


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
    client_sockets, messages, names = [], [], dict()
    logger.debug('The socket is ready to receive messages')

    while True:
        try:
            client, address = server_socket.accept()
        except OSError as e:
            print(e.errno)
        else:
            client_sockets.append(client)
        finally:
            write_sock, read_sock = [], []
            try:
                if client_sockets:
                    write_sock, read_sock, err_sock = select.select(client_sockets, client_sockets, [], 0)
            except OSError as e:
                print(e.errno)

            if write_sock:
                for client in write_sock:
                    try:
                        process_client_message(get_message(client),
                                               messages, client, client_sockets, names)
                    except Exception:
                        print(f'The client {client.getpeername()} disconnected from the server.')
                        client_sockets.remove(client)
            for i in messages:
                try:
                    process_message(i, names, read_sock)
                except Exception:
                    print(f'Communication with client {i[DESTINATION]} was lost.')
                    client_sockets.remove(names[i[DESTINATION]])
                    del names[i[DESTINATION]]
            messages.clear()


if __name__ == '__main__':
    main()
