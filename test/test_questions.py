"test user table arguments"
import json
import unittest
import time
from flask_jwt_extended import create_access_token
from app.models.questions_model import Questions
from app.models.user_model import Users
from app.models import database_connection
from app.resources.questions.questions import post_question
from app import create_app
from .base import BaseTest

class TestQUestion(BaseTest):
    """
    test user table arguments
    """

    def test_question_update(self):
        """
        update question test
        """
        new_question={
        "title":"this is my edited quiz",
        "description":"this is my edited description"
        }
        cursor=self.question.search_question_by_questionid(1,self.connection.cursor())
        find_question=cursor.fetchall()
        if find_question:
            self.question.update_question(new_question["title"],
                                            new_question["description"],
                                            1,self.connection.cursor())
            cursor=self.question.search_question_by_questionid(1,self.connection.cursor())
            find_question=cursor.fetchall()
            self.assertEqual(new_question["title"],find_question[0][1])

    def test_question_delete(self):
        """
        test question from the database
        """
        cursor=self.question.fetch_all_question(self.connection.cursor())
        length_one = cursor.fetchall()
        self.question.delete_question(2,self.connection.cursor())
        cursor = self.question.fetch_all_question(self.connection.cursor())
        length_two = cursor.fetchall()
        self.assertEqual(len(length_one)-1,len(length_two))

    def test_fetch_all_question_api(self):
        """
        fetch all question from the database
        """
        response = self.app.get("/api/v1/questions")
        data = response.get_json()
        self.assertEqual(response.status_code,401)

    def test_ask_question_api_without_login(self):
        """
        userr post question api endpoints test
        """
        url = "/api/v1/add_question"
        response = self.app.post(url,data = json.dumps(self.question_sample), headers = self.headers)
        self.assertEqual(response.status_code,201)

    def test_update_question_api_without_login(self):
        """
        should forbid unauthorized user when posting question
        """
        url = "api/v1/update_question/1"
        update_question = {
        "title":self.question_sample["title"],
        "description":self.question_sample["description"]
        }
        response = self.app.put(url,data = json.dumps(update_question),headers = self.headers)
        self.assertEqual(response.status_code,200)

    def test_delete_question_api(self):
        """
        should forbid unauthorized user from deleting question
        """
        url = "/api/v1/delete_question/1"
        response = self.app.delete(url)
        self.assertEqual(response.status_code,401)

    def test_ask_question_with_login(self):
        """
        userr post question api endpoints test
        """
        url= "/api/v1/add_question"
        response=self.app.post(url,data = json.dumps(self.question_data), headers =self.headers)
        self.assertEqual(response.status_code,201)

    def test_ask_question_with_login_error(self):
        """
        userr post question api endpoints test
        """
        url= "/api/v1/add_question"
        response=self.app.post(url,data = json.dumps(self.question_data), headers =self.headers)
        self.assertEqual(response.status_code,201)

    def test_update_question_with_login_error(self):
        """update question with login"""
        url = "api/v1/update_question/1"
        response = self.app.put(url,data = json.dumps(self.question_data),headers = self.headers)

    def test_fetch_all_question_api_with_login(self):
        """
        fetch all question from the database
        """
        question_data={"title":"this is my first question",
            "description":"this is just a description"}

        response=self.app.get("/api/v1/questions",headers=self.headers)
        data = response.get_json()
        self.assertEqual(response.status_code,200)

    def test_fetch_specific_question(self):
        """fetch a specific question with login"""
        question_data={"title":"this is my first question",
            "description":"this is just a description"}
        url ="/api/v1/questions/1"
        response=self.app.get(url,headers=self.headers)
        self.assertEqual(response.status_code,200)

    def test_fetch_specific_question_with_error(self):
        """fetch a specific question with login"""
        url ="/api/v1/questions/1"
        response=self.app.get(url,headers=self.headers)
        self.assertEqual(response.status_code,200)

    def test_update_question_with_empty_body(self):
        """update question with login"""

        url = "api/v1/update_question/2"
        update_question = {
        "title":"",
        "description":self.question_sample["description"]
        }
        response = self.app.put(url,data = json.dumps(update_question),headers = self.headers)
        self.assertEqual(response.status_code,400)
