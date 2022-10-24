import json
from chatapp.common.variables import MAX_PACKAGE_LENGTH, ENCODING


def send_message(sock, message):
    sock.send(json.dumps(message).encode(ENCODING))


def get_message(sock):
    message = json.loads(sock.recv(MAX_PACKAGE_LENGTH))
    print(message)
    return message
