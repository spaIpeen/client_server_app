import json
import sys
from functools import wraps
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
sys.path.append('..')
import logging
import logs.client_log_config
import logs.server_log_config


def log(func):
    @wraps(func)
    def wrap(*args):
        name = f'{sys.argv[0].split("/")[-1][:-3]}'
        logger = logging.getLogger(f'chatapp.{name}')
        if name == 'client':
            logger.info(f'Function {func.__name__}() calls from function {sys._getframe(1).f_code.co_name}()')
            logger.info(f'{args}')
        elif name == 'server':
            logger.info(f'Function {func.__name__}() calls from function {sys._getframe(1).f_code.co_name}()')
            logger.info(f'{args}')
        return func(*args)
    return wrap


@log
def send_message(sock, message):
    if not isinstance(message, str):
        raise TypeError
    sock.send(message.encode(ENCODING))


@log
def get_message(sock):
    bytes_message = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(bytes_message, bytes):
        str_message = bytes_message.decode(ENCODING)
        if isinstance(str_message, str):
            print(str_message)
            return str_message
        raise ValueError
    raise ValueError
