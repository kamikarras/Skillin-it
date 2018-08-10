from model import db, connect_to_db
from server import app
import unittest

# this is the test file

class MyAppIntergrationTestCase(unittest.TestCase):
    """tests for skillin it"""

    def setUp(self):
        """code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage_page(self):
        """can we reach the homepage"""

        result = self.client.get("/")
        self.assertIn(b"a project by Kami Karras", result.data)

    def test_register_page(self):
        """can we reach the register form"""

        result = self.client.get("/register")
        self.assertIn(b"<form action='/register' method='POST'>", result.data)
    def test_login_page(self):
        """can we reach the login form"""

        result = self.client.get("/login")
        self.assertIn(b"<form action='/login' method='POST'>", result.data)




if __name__ == "__main__":
    unittest.main()
