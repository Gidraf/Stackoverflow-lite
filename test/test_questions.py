"test user table arguments"
import unittest
import time
from app.models.questions_model import Questions
from app.models.user_model import Users


class TestQUestion(unittest.TestCase):
    "test user table arguments"

    def setUp(self):
        "setup database"
        self.question=Questions()
        self.question.create_question_table()
        self.user=Users()
        self.questio_sample={
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

    def tearDown(self):
        "teardown test"
        self.question.clear_question_table()
        self.user.clear_user_table()


    def test_question_add(self):
        "test if queston has been saved to database"
        self.user.register_user(**self.user_sample)
        self.question.add_question(**self.questio_sample)
        ask_question=self.question.search_question_by_title(self.questio_sample["title"])
        self.assertEqual(title,ask_question[0][1])
