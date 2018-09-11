import unittest
import json
import psycopg2.extras
from datetime import datetime
from flask import url_for
from flask import request
from flask import jsonify
from app import create_app
from app.models.user_model import Users
from app.models.questions_model import Questions
from app.models.answers_model import Answers
from app.models import database_connection

class TestAnswer(unittest.TestCase):
    """
    test answers
    """

    def setUp(self):
        """
        setup database
        setuo server
        """
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
        answer_url="/api/v1/answers/1"
        self.answer_text="this is just an answer"
        self.answer.add_answer(self.answer_text,datetime.utcnow(),1,1,0,False,self.connection.cursor())
        self.app.post(answer_url,data=json.dumps(self.answer_text),headers=self.headers)
        self.app.post(answer_url,data=json.dumps(self.answer_text),headers=self.headers)

    def tearDown(self):
        """
        tear down method
        destroy datas saved on the database
        """
        self.user.clear_user_table(self.connection)
        self.question.clear_question_table(self.connection)
        self.answer.clear_answer_table(self.connection)

    def test_mark_answer_as_prefered(self):
        """
        test if user can answer
        """
        answer_text="hello"
        url="/api/v1/prefered_answer/1"
        response=self.app.patch(url,data = json.dumps(answer_text), headers = self.headers)
        self.assertEqual(response.status_code,200)

    def test_mark_answer_as_prefered_not_found(self):
        """
        test if user can answer
        """
        answer_text="hello"
        url="/api/v1/prefered_answer/2"
        response=self.app.patch(url,data = json.dumps(answer_text), headers = self.headers)
        self.assertEqual(response.status_code,404)

    def test_mark_answer_as_prefered_another_user_question(self):
        """test if user can answer"""
        answer_text="hello"
        url="/api/v1/prefered_answer/1"
        login_url="/auth/login"
        login_response=self.app.post(login_url, data=json.dumps({
                "username": "orenja",
                "password": "Winners11"
                }),headers = self.headers)

        token=login_response.json
        header={"Authorization":"Bearer "+token["token"],'Content-Type': "application/json"}
        response=self.app.patch(url,data = json.dumps(answer_text), headers = header)
        self.assertEqual(response.status_code,403)

    def test_add_answer_to_question(self):
        """
        test should return true if the answer is successfully added to the database on server
        """
        answer_text={"answer_text":"hello"}
        url="/api/v1/answers/1"
        response=self.app.post(url,data = json.dumps(answer_text), headers = self.headers)
        self.assertEqual(response.status_code,201)

    def test_get_answers_to_a_question(self):
        """
        test should return 200 response code
        """
        url="/api/v1/answers/1"
        response=self.app.get(url, headers = self.headers)
        self.assertEqual(response.status_code,200)

    def test_get_answers_to_a_question_not_found(self):
        """
        test should return 200 response code
        """
        url="/api/v1/answers/88"
        response=self.app.get(url, headers = self.headers)
        self.assertEqual(response.status_code,404)

    def test_add_answer_to_question_not_foune(self):
        """
        response should be 404
        """
        answer_text={"answer_text":"hello"}
        url="/api/v1/answers/7"
        response=self.app.post(url,data = json.dumps(answer_text), headers = self.headers)
        self.assertEqual(response.status_code,404)

    def test_add_answer_to_question_with_empty_answer_text(self):
        """
        test should return 400 request code if the answer is successfully added to the database on server
        """
        answer_text={"answer_text":""}
        url="/api/v1/answers/1"
        response=self.app.post(url,data = json.dumps(answer_text), headers = self.headers)
        self.assertEqual(response.status_code,400)

    def test_display_error_message_when_posting_empty_body(self):
        """test if user can answer"""
        url="/api/v1/answers/1"
        answer_text={}
        response=self.app.post(url, data=answer_text, headers = self.headers)
        self.assertEqual(response.status_code,400)
