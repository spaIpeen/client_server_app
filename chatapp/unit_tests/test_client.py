import unittest
from client import generate_presence
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME


class TestClient(unittest.TestCase):
    message = {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}}

    def test_generate_presence(self):
        dict_check = generate_presence()
        dict_check[TIME] = 1
        self.assertEqual(dict_check, self.message)


if __name__ == "__main__":
    unittest.main()
