import json
import sys
from functools import wraps
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
sys.path.append('..')
import logging
import logs.client_log_config
import logs.server_log_config

logger_client = logging.getLogger('chatapp.client')
logger_server = logging.getLogger('chatapp.server')


def log(func):
    @wraps(func)
    def wrap(*args):
        name = f'{sys.argv[0].split("/")[-1][:-3]}'
        if name == 'client':
            logger_client.info(f'Function {func.__name__}() calls from function {sys._getframe(1).f_code.co_name}()')
            logger_client.info(f'{args}')
        elif name == 'server':
            logger_server.info(f'Function {func.__name__}() calls from function {sys._getframe(1).f_code.co_name}()')
            logger_server.info(f'{args}')
        return func(*args)
    return wrap


@log
def send_message(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    sock.send(json.dumps(message).encode(ENCODING))


@log
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
