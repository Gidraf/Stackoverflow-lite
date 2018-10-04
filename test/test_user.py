import unittest
import json
import psycopg2.extras
from flask import url_for
from flask import request
from flask import jsonify
from app import create_app
from app.models.user_model import Users
from app.models.comments_model import Comments
from app.models.votes_model import Votes
from app.models import database_connection
class TestUser(unittest.TestCase):
    """
    test user table class
    """

    def setUp(self):
        """
        setup database
        """
        init_app=create_app("testing")
        self.app = init_app.test_client()
        self.app.testing = True
        self.connection = database_connection("test")
        self.user = Users()
        self.user.create_user_table(self.connection)
        self.comment = Comments()
        self.votes = Votes()
        self.user_sample={
        "username":"orenja",
        "useremail":"orenjagidraf@gmal.com",
        "password":"Winners11"
        }
        self.user.register_user(self.user_sample["username"],self.user_sample["useremail"],
                                self.user_sample["password"],self.connection.cursor())
        self.headers = {'Content-Type': "application/json"}

    def tearDown(self):
        """
        tear down method
        destroy datas saved on the database
        """
        self.user.clear_user_table(self.connection)
        self.user.clear_user_table(self.connection)
        self.comment.clear_comment_table(self.connection)
        self.votes.clear_votes_table(self.connection)

    def test_registration_of_user_api(self):
        """
        test if the response status code == 201
        """
        current_user={
        "username":"gidraf",
        "useremail":"userame@gmail.com",
        "password":"test"
        }
        url="/auth/register"
        response=self.app.post(url, data = json.dumps(current_user), headers = {'Content-Type': "application/json"})
        self.assertEqual(response.status_code,201)

    def test_registration_of_user_with_username_error(self):
        """
        test if the response is 201
        """
        url="/auth/register"
        current_user={
        "username":"gidraf/",
        "useremail":"username@gmail.com",
        "password":"test"
        }
        response=self.app.post(url,data=json.dumps(current_user),headers=self.headers)
        self.assertEqual(response.status_code,400)

    def test_registration_of_user_with_error_email(self):
        """
        test if the response is 201
        """
        url="/auth/register"
        current_user={
        "username":"gidraf",
        "useremail":"usernamegmail.com",
        "password":"test"
        }
        response=self.app.post(url,data=json.dumps(current_user),headers=self.headers)
        self.assertEqual(response.status_code,400)

    def test_registration_of_user_with_empty(self):
        """
        test if the response is 201
        """
        url="/auth/register"
        current_user={
        "username":"",
        "useremail":"usernamegmail.com",
        "password":"test"
        }
        response=self.app.post(url,data=json.dumps(current_user),headers=self.headers)
        self.assertEqual(response.status_code,400)

    def test_login_of_user(self):
        """
        test if user can login and authenticated
        """
        credentials={
        "username":"orenja",
        "password":"Winners11"
        }
        url="/auth/login"
        response=self.app.post(url,data=json.dumps(credentials),headers=self.headers)
        self.assertEqual(response.status_code,200)


    def test_login_of_user_wth_error(self):
        """
        test if user can login and authenticated
        """
        url="/auth/login"
        credentials ={
                "username": "",
                "password": ""
                }
        response=self.app.post(url,data=json.dumps(credentials),headers=self.headers)
        self.assertEqual(response.status_code,400)

    def test_login_of_user_with_wrong_password(self):
        """
        test if user can login and authenticated
        """
        url="/auth/login"
        credentials ={
                "username": self.user_sample["username"],
                "password": "hgghg"
                }
        response=self.app.post(url,data=json.dumps(credentials),headers=self.headers)
        self.assertEqual(response.status_code,401)
