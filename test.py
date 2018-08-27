# from model import db, connect_to_db
# from server import app
import unittest
from selenium import webdriver

# this is the test file

class MyAppTest(unittest.TestCase):
    """tests for skillin it"""

    def setUp(self):
        """code to run before every test."""

        self.browser = webdriver.Chrome()

    def tearDown(self):
        """test closing"""
        self.browser.quit()

    def test_title(self):
        """tests the title"""
        self.browser.get('http://localhost:5000/')
        self.assetEqual(self.browser.title, 'Skillin it')


    # def test_homepage_page(self):
    #     """can we reach the homepage"""

    #     result = self.client.get("/")
    #     self.assertIn(b"a project by Kami Karras", result.data)

    # def test_register_page(self):
    #     """can we reach the register form"""

    #     result = self.client.get("/register")
    #     self.assertIn(b"<form action='/register' method='POST'>", result.data)
    # def test_login_page(self):
    #     """can we reach the login form"""

    #     result = self.client.get("/login")
    #     self.assertIn(b"<form action='/login' method='POST'>", result.data)




if __name__ == "__main__":
    unittest.main()
