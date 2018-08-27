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

class TestQUestion(unittest.TestCase):
    """
    test user table arguments
    """

    def setUp(self):
        """setup database"""
        init_app=create_app("testing")
        init_app.config["TESTING"]=True
        init_app.config["LOGIN_DISABLED"]=True
        self.app=init_app.test_client()
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


    def test_question_add_question_searched(self):
        """
        test if queston has been saved to database
        """
        cursor=self.question.search_question_by_title(self.question_sample["title"],self.connection.cursor())
        searched_question=cursor.fetchall()
        title=searched_question[0][1]
        self.assertEqual(title,self.question_sample["title"])

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
        cursor=self.question.fetch_all_question(self.connection.cursor())
        length_two = cursor.fetchall()
        self.assertEqual(len(length_one)-1,len(length_two))

    def test_fetch_all_question_api(self):
        """
        fetch all question from the database
        """
        response=self.app.get("/api/v1/questions")
        data = response.get_json("questions")
        title = data["questions"][0][1]
        self.assertEqual(response.status_code,200)
        self.assertEqual(title,self.question_sample["title"])

    def test_ask_question_api(self):
        """
        userr post question api endpoints test
        """
        url= "/api/v1/add_question"
        response=self.app.post(url,data = json.dumps(self.question_sample), headers = self.headers)
        self.assertEqual(response.status_code,401)

    def test_update_question_api(self):
        """
        should forbid unauthorized user when posting question
        """
        url = "api/v1/update_question/1"
        update_question = {
        "title":self.question_sample["title"],
        "description":self.question_sample["description"]
        }
        response = self.app.put(url,data = json.dumps(update_question),headers = self.headers)
        self.assertEqual(response.status_code,401)

    def test_delete_question_api(self):
        """
        should forbid unauthorized user from deleting question
        """
        url = "/api/v1/delete_question/1"
        response = self.app.delete(url)
        self.assertEqual(response.status_code,401)

    #def test_question_search
