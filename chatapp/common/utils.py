import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING


def send_message(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    sock.send(json.dumps(message).encode(ENCODING))


def get_message(sock):
    bytes_message = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(bytes_message, bytes):
        str_message = bytes_message.decode(ENCODING)
        if isinstance(str_message, str):
            dict_message = json.loads(str_message)
            if isinstance(dict_message, dict):
                print(dict_message)
                return dict_message
            raise ValueError
        raise ValueError
    raise ValueError
