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
from app.models.comments_model import Comments
from app.models.votes_model import Votes
from app.models import database_connection

class TestQUestion(unittest.TestCase):
    """
    test user table
    """

    def setUp(self):
        """
        setup database
        setup server
        """
        init_app=create_app("testing")
        self.app = init_app.test_client()
        self.app.testing = True
        self.connection = database_connection("test")
        self.user = Users()
        self.answers = Answers()
        self.user.create_user_table(self.connection)
        self.question = Questions()
        self.question.create_question_table(self.connection)
        self.comments = Comments()
        self.votes = Votes()
        self.question_sample = {
        "title":"my questiohjhj jn",
        "description":"this is my descriotion",
        }
        self.question_sample_two = {
        "title":"another question of mine",
        "description":"this is my descrioption"
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
        self.question_data={"title":"bfg jfjg ngjf dngkjf",
            "description":"this is just a description"}
        self.headers = {'Content-Type': "application/json"}
        reg_url="/auth/register"
        self.app.post(reg_url,data=json.dumps(self.user_sample),headers=self.headers)
        self.app.post(reg_url,data=json.dumps(self.user_sample_two),headers=self.headers)
        login_url="/auth/login"
        login_response=self.app.post(login_url, data=json.dumps({
                "username": "wiliam",
                "password": "Winners11"
                }),headers=self.headers)
        token=login_response.json
        self.headers={"Authorization":"Bearer "+token["token"],'Content-Type': "application/json"}
        question_url = "api/v1/add_question"
        self.app.post(question_url, data = json.dumps(self.question_sample), headers = self.headers)
        self.app.post(question_url, data = json.dumps(self.question_sample_two), headers = self.headers)
        self.app.post(question_url, data = json.dumps(self.question_data), headers = self.headers)

    def tearDown(self):
        """
        tear down method
        destroy data saved in the database
        """
        self.user.clear_user_table(self.connection)
        self.question.clear_question_table(self.connection)
        self.answers.clear_answer_table(self.connection)
        self.comments.clear_comment_table(self.connection)
        self.votes.clear_votes_table(self.connection)

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

    def test_search_question_by_string(self):
        '''string search by name test'''
        string = "my "
        cursor = self.question.search_question_by_name(string,self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        question = cursor.fetchall()
        self.assertEqual(question[0]["title"],"my questiohjhj jn")

    def test_question_with_title_error(self):
        """
        user post question witj empty question api endpoints test
        """
        question_data={
        "title":"",
        "description":"fkjfkjdkfjejrof"
        }
        url= "/api/v1/add_question"
        response=self.app.post(url,data = json.dumps(question_data), headers =self.headers)
        self.assertEqual(response.status_code,400)

    def test_question_with_descripption_error(self):
        """
        user post question witj empty question api endpoints test
        """
        question_data={
        "title":"hhh",
        "description":""
        }
        url= "/api/v1/add_question"
        response=self.app.post(url,data = json.dumps(question_data), headers =self.headers)
        self.assertEqual(response.status_code,400)

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
        self.assertEqual(response.status_code,200)

    def test_update_question_api_without_login(self):
        """
        should forbid unauthorized user when posting question
        """
        url = "api/v1/update_question/1"
        update_question = {
        "title":self.question_sample["title"],
        "description":self.question_sample["description"]
        }
        response = self.app.put(url,data = json.dumps(update_question),headers = {'Content-Type': "application/json"})
        self.assertEqual(response.status_code,401)

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
        question_data={
        "title":"nnnnnnn",
        "description":"fkjfkjdkfjejrof"
        }
        url= "/api/v1/add_question"
        response=self.app.post(url,data = json.dumps(question_data), headers =self.headers)
        self.assertEqual(response.status_code,201)

    def test_ask_question_that_exist_api(self):
        """
        as a user I should be able to post a question
        """
        question_sample_two = {
        "title":"another question of mine",
        "description":"this is my descrioption"}
        question_url = "api/v1/add_question"
        response = self.app.post(question_url,data=json.dumps(question_sample_two),headers=self.headers)
        self.assertEqual(response.status_code,400)

    def test_update_question_that_exist_api(self):
        """
        as a user I should be able to post a question
        """
        question_sample_two = {
        "title":"another question of mine",
        "description":"this is my descrioption"}
        question_url = "api/v1/update_question/1"
        response = self.app.put(question_url,data=json.dumps(question_sample_two),headers=self.headers)
        self.assertEqual(response.status_code,400)

    def test_ask_question_with_login_error(self):
        """
        userr post question api endpoints test
        """
        url= "/api/v1/add_question"
        response=self.app.post(url,data = json.dumps(self.question_data), headers ={"Content-Type":"application/json"})
        self.assertEqual(response.status_code,401)

    def test_update_question_with_login(self):
        """update question with login"""
        url = "api/v1/update_question/1"
        new_question={
        "title":"ghhhghg",
        "description":"ffgfjgfj"
        }
        response = self.app.put(url,data = json.dumps(new_question),headers = self.headers)
        self.assertEqual(response.status_code,200)

    def test_update_question_already_exists_with_login(self):
        """update question with login"""
        url = "api/v1/update_question/1"
        new_question={
        "title":"my quesnjjtion",
        "description":"this is my descriotion"
        }
        response = self.app.put(url,data = json.dumps(new_question),headers = self.headers)
        self.assertEqual(response.status_code,200)

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
        question_data = {"title":"this is my first question",
            "description":"this is just a description"}
        url = "/api/v1/questions/1"
        response = self.app.get(url,headers=self.headers)
        self.assertEqual(response.status_code,200)

    def test_fetch_specific_question_not_found(self):
        """fetch a specific question with login"""
        url ="/api/v1/questions/550000"
        response=self.app.get(url,headers=self.headers)
        self.assertEqual(response.status_code,404)

    def test_update_question_with_empty_body(self):
        """update question with login"""
        url = "api/v1/update_question/2"
        update_question = {
        "title":"",
        "description":self.question_sample["description"]
        }
        response = self.app.put(url,data = json.dumps(update_question),headers = self.headers)
        self.assertEqual(response.status_code,400)

    def test_update_question_with_empty_description(self):
        """update question with login"""
        url = "api/v1/update_question/2"
        update_question = {
        "title":"ndndnf",
        "description":""
        }
        response = self.app.put(url,data = json.dumps(update_question),headers = self.headers)
        self.assertEqual(response.status_code,400)

    def test_update_question_another_person_question(self):
        """update question with login"""
        url = "api/v1/update_question/3"
        update_question = {
        "title":"ndndnf",
        "description":"jhjhjhj"
        }
        login_url="/auth/login"
        login_response=self.app.post(login_url, data=json.dumps({
                "username": "orenja",
                "password": "Winners11"
                }),headers=self.headers)
        token=login_response.json
        header={"Authorization":"Bearer "+token["token"],'Content-Type': "application/json"}
        response = self.app.put(url,data = json.dumps(update_question),headers = header)
        self.assertEqual(response.status_code,403)
