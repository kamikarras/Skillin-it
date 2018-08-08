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

    def test_homepage(self):
        """can we reach the homepage"""

        result = self.client.get("/")
        self.assertIn(b"a project by Kami Karras", result.data)


if __name__ == "__main__":
    unittest.main()
