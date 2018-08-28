"""test answers model"""
import unittest
import json
from flask import url_for
from flask import request
from flask import jsonify
from app import create_app

class TestAnswer(unittest.TestCase):
    """test answers"""

    def setUp(self):
        """setup database"""
        init_app=create_app("testing")
        self.app = init_app.test_client()
        self.connection = database_connection("test")
        self.user = Users()
        self.user.create_user_table(self.connection)
        self.question = Questions()
        self.question.create_question_table(self.connection)
        self.question_sample = {
        "title":"my question",
        "description":"this is my descriotion",
        "time_created":time.time(),
        "userid":1
        }

        self.user_sample={
        "username":"gidraf",
        "useremail":"orenjagidraf@gmal.com",
        "password":"Winners11"
        }

        self.answer_sample={
        "answer_text":"this is  my sample answer",

            }
        self.user.register_user(self.user_sample["username"],self.user_sample["useremail"],
                                self.user_sample["password"],self.connection.cursor())
        self.question.add_question(self.question_sample["title"],self.question_sample["description"],
                                    self.question_sample["time_created"],self.question_sample["userid"],
                                    self.connection.cursor())
        self.question.add_question(self.question_sample["title"],self.question_sample["description"],
                                    self.question_sample["time_created"],self.question_sample["userid"],
                                    self.connection.cursor())
        self.data_type = "application/json"
        self.headers = {
            'Content-Type': self.data_type,
            'Accept': self.data_type}

    def tearDown(self):
        """
        teardown test
        """
        self.question.clear_question_table(self.connection)
        self.user.clear_user_table(self.connection)
