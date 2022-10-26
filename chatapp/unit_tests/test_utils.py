import json
import unittest

from common.utils import send_message, get_message
from common.variables import ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ALERT


class TestSocket(unittest.TestCase):

    def __init__(self, test_dict):
        super().__init__()
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    test_client_send = {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}}
    test_get_serv_dict_ok = {RESPONSE: 200, ALERT: "OK"}
    test_get_serv_dict_err = {RESPONSE: 400, ALERT: "BAD REQUEST"}

    def test_send_ok(self):
        test_socket = TestSocket(self.test_client_send)
        send_message(test_socket, self.test_client_send)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_send_error(self):
        test_socket = TestSocket(self.test_client_send)
        send_message(test_socket, self.test_client_send)
        self.assertRaises(TypeError, send_message, test_socket, 'string')

    def test_get_ok(self):
        test_socket_ok = TestSocket(self.test_get_serv_dict_ok)
        self.assertEqual(get_message(test_socket_ok), self.test_get_serv_dict_ok)

    def test_get_error(self):
        test_socket_err = TestSocket(self.test_get_serv_dict_err)
        self.assertEqual(get_message(test_socket_err), self.test_get_serv_dict_err)


if __name__ == "__main__":
    unittest.main()
