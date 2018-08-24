"test user table arguments"
import unittest
import time
from app.models.questions_model import Questions


class TestQUestion(unittest.TestCase):
    "test user table arguments"

    def setUp(self):
        "setup database"
        self.question=Questions()
        self.question.create_question_table()

    def tearDown(self):
        "teardown test"
        self.question.clear_question_table()


    def test_question_add(self):
        "test if queston has been saved to database"
        title="my question"
        description="this is my descriotion"
        time_created=time.time()
        userid=2
        self.question.add_question(title,description,time_created,userid)
        ask_question=self.question.search_question_by_title(title)
        self.assertEqual(title,ask_question[0][1])
