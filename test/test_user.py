import unittest
from app.models.user_model import Users


class TestUser(unittest.TestCase):
    "test user table class"

    def setUp(self):
        self.user=Users()
        self.user.create_user_table()

    def tearDown(self):
        self.user.clear_user_table()

    def test_test_registration(self):
        "test if user has been registered successfully"
        username="username"
        useremail="username@gmail.com"
        password="Winners11"
        self.user.register_user(username,useremail,password)
        reg_username=self.user.search_user_by_username(username)
        self.assertEqual(username,reg_username[0][1])
