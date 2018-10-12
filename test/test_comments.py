"""
this module hold the tests for comment
"""
import unittest
import json
import psycopg2.extras
from datetime import datetime
from flask import url_for
from flask import request
from flask import jsonify
from app import create_app
from app.models.user_model import Users
from app.models.comments_model import Comments
from app.models.answers_model import Answers
from app.models.questions_model import Questions
from app.models.votes_model import Votes
from app.models import database_connection


class TestComments(unittest.TestCase):
    """
    holds test cases for coments models
    """

    def setUp(self):
        """setup database data used for testing"""
        init_app=create_app("testing")
        self.app = init_app.test_client()
        self.app.testing = True
        self.connection = database_connection("test")
        self.user = Users()
        self.user.create_user_table(self.connection)
        self.question = Questions()
        self.question.create_question_table(self.connection)
        self.answer=Answers()
        self.answer.create_answer_table(self.connection)
        self.comment = Comments()
        self.comment.create_comment_table(self.connection)
        self.votes = Votes()
        self.votes.create_votes_table(self.connection)
        self.question_sample = {
        "title":"my question",
        "description":"this is my descriotion",
        }
        self.question_sample_two = {
        "title":"another question of mine",
        "description":"this is my descrioption",
        }
        self.user_sample={
        "username":"wiliam",
        "useremail":"gidraf@gmal.com",
        "password":"Winners11"
        }
        self.user_sample_two={
        "username":"orenja",
        "useremail":"orenja@gmal.com",
        "password":"Winners11"
        }
        self.question_data={"title":"this is my first question",
            "description":"this is just a description"}
        self.headers = {'Content-Type': "application/json"}
        reg_url="/auth/register"
        self.app.post(reg_url,data=json.dumps(self.user_sample),headers = self.headers)
        self.app.post(reg_url,data=json.dumps(self.user_sample_two),headers = self.headers)
        login_url="/auth/login"
        login_response=self.app.post(login_url, data=json.dumps({
                "username": "wiliam",
                "password": "Winners11"
                }),headers = self.headers)

        token=login_response.json
        self.headers={"Authorization":"Bearer "+token["token"],'Content-Type': "application/json"}
        question_url="api/v1/add_question"
        self.app.post(question_url,data=json.dumps(self.question_sample_two),headers=self.headers)
        self.app.post(question_url,data=json.dumps(self.question_sample),headers=self.headers)
        self.app.post(question_url,data=json.dumps(self.question_data),headers=self.headers)
        answer_url = "/api/v1/answers/1"
        answer_text = {"answer_text":"this is just an answer"}
        answer_text_two = {"answer_text":"this is answer"}
        self.app.post(answer_url,data=json.dumps(answer_text), headers = self.headers)
        self.app.post(answer_url,data=json.dumps(answer_text_two), headers = self.headers)

    def tearDown(self):
        """
        tear down method
        destroy datas saved on the database
        """
        self.user.clear_user_table(self.connection)
        self.question.clear_question_table(self.connection)
        self.answer.clear_answer_table(self.connection)
        self.comment.clear_comment_table(self.connection)
        self.votes.clear_votes_table(self.connection)

    def test_add_comment(self):
        """
        test insert user comment to the database
        test should pass if the comment is successfully inserted to the database
        """
        data = {
        "comment_text":"ttttt ttt tttt ttt"
        }
        url = "/api/v1/add_comment/2"
        cursor = self.answer.search_answer_by_id(1, self.connection.cursor())
        response = self.app.post(url,data = json.dumps(data),headers = self.headers)
        self.assertEqual(response.status_code,201)
