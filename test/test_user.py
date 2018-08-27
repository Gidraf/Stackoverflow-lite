import unittest
import json
from app.models.user_model import Users
from app.models import database_connection
from app import create_app


class TestUser(unittest.TestCase):
    """
    test user table class
    """

    def setUp(self):
        init_app=create_app("testing")
        init_app.config["TESTING"]=True
        self.app=init_app.test_client()
        self.connection=database_connection("test")
        self.user=Users()
        self.user.create_user_table(self.connection)
        self.current_user={
        "username":"gidraf",
        "useremail":"username@gmail.com",
        "password":"test"
        }
        self.data_type = "application/json"
        self.headers = {
            'Content-Type': self.data_type,
            'Accept': self.data_type}

    def tearDown(self):
        self.user.clear_user_table(self.connection)

    def test_test_registration(self):
        """
        test if user has been registered successfully
        """
        self.user.register_user(self.current_user["username"],self.current_user["useremail"],self.current_user["password"],self.connection.cursor())
        cursor=self.user.search_user_by_username(self.current_user["username"],self.connection.cursor())
        reg_username=cursor.fetchall()
        self.assertEqual(self.current_user["username"],reg_username[0][1])

    def test_registration_of_user_api(self):
        """
        test if the response is 201
        """
        url="/auth/register"
        response=self.app.post(url,data=json.dumps(self.current_user),headers=self.headers)
        self.assertEqual(response.status_code,200)

        """def test_login_of_user(self):

            test if user can login and authenticated
    
            self.user.register_user(self.current_user["username"],self.current_user["useremail"],
                                    self.current_user["password"],self.connection.cursor())
            cursor=self.user.search_user_by_username(self.current_user["username"],self.connection.cursor())
            reg_username=cursor.fetchall()
            url="/auth/login"
            credentials ={
                    "username": self.current_user["username"],
                    "password": self.current_user["password"]
                    }
            response=self.app.post(url,data=json.dumps(credentials),headers=self.headers)
            data=dict(response.get_json("success"))
            success=data["success"]
            self.assertEqual(success,"your access token is")
            self.assertEqual(response.status_code,200)
            """
