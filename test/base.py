import unittest
import json
from flask import url_for
from flask import request
from flask import jsonify
from app import create_app
from app.models.user_model import Users
from app.models.answers_model import Answers
from app.models.questions_model import Questions
from app.models import database_connection


class BaseTest(unittest.TestCase):
    """base class to hold the setup function of our code"""
    def setUp(self):
        """setup database"""
        init_app=create_app("testing")
        self.app = init_app.test_client()
        self.connection = database_connection("test")
        self.user = Users()
        self.user.create_user_table(self.connection)
        self.question = Questions()
        self.question.create_question_table(self.connection)
        self.answers=Answers()
        self.answers.create_answer_table(self.connection)
        self.question_sample = {
        "title":"my question",
        "description":"this is my descriotion",
        "time_created":"time.time()",
        "userid":1
        }

        self.user_sample={
        "username":"gidraf",
        "useremail":"orenjagidraf@gmal.com",
        "password":"Winners11"
        }
        self.question_data={"title":"this is my first question",
            "description":"this is just a description"}
        self.answer_sample={
        "answer_text":"this is  my sample answer",

            }
        self.current_user={
        "username":"gidraf",
        "useremail":"username@gmail.com",
        "password":"test"
        }
        self.user.register_user(self.user_sample["username"],self.user_sample["useremail"],
                                self.user_sample["password"],self.connection.cursor())
        self.question.add_question(self.question_sample["title"],self.question_sample["description"],
                                    self.question_sample["time_created"],self.question_sample["userid"],
                                    self.connection.cursor())
        self.question.add_question(self.question_sample["title"],self.question_sample["description"],
                                    self.question_sample["time_created"],self.question_sample["userid"],
                                    self.connection.cursor())
        answer_text="hello"
        time="now"
        vote=0
        is_answer=False
        questionid=1
        userid=1
        self.answers.add_answer(answer_text,time,1,1,0,is_answer,self.connection.cursor())
        answer_list = self.answers.search_answer_by_questionid(questionid,self.connection.cursor())
        self.headers = {'Content-Type': "application/json"}
        login_url="/auth/login"
        login_response=self.app.post(login_url, data=json.dumps({
                "username": "gidraf",
                "password": "test"
                }),headers=self.headers)
        token=login_response.json
        self.headers={"Authorization":"Bearer "+token["token"],'Content-Type': "application/json"}
        url="/api/v1/answers/1"

    def tearDown(self):
        """
        teardown test
        """
        self.question.clear_question_table(self.connection)
        self.user.clear_user_table(self.connection)
        self.answers.clear_answer_table(self.connection)
