import unittest

from common.variables import RESPONSE, ALERT, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME
from server import generate_response


class TestServer(unittest.TestCase):
    test_response_ok = {RESPONSE: 200, ALERT: "OK"}
    test_response_err = {RESPONSE: 400, ALERT: "BAD REQUEST"}

    def test_ok(self):
        self.assertEqual(generate_response({ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.test_response_ok)

    def test_err_wrong_action(self):
        self.assertEqual(generate_response({ACTION: 'OK', TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.test_response_err)

    def test_err_no_action(self):
        self.assertEqual(generate_response({TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.test_response_err)

    def test_err_no_time(self):
        self.assertEqual(generate_response({ACTION: 'OK', USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.test_response_err)

    def test_err_no_user(self):
        self.assertEqual(generate_response({ACTION: 'OK', TIME: 1}),
                         self.test_response_err)

    def test_err_wrong_user(self):
        self.assertEqual(generate_response({ACTION: 'OK', TIME: 1, USER: {ACCOUNT_NAME: 'User'}}),
                         self.test_response_err)


if __name__ == "__main__":
    unittest.main()
