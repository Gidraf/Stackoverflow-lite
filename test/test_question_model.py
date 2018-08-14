"""this model should test question models"""
import pytest
from app.models.models import Question



@pytest.fixture
def questions_list():
    '''questions list initialization'''
    question = [{
        "id": 1,
        "title": "what is my name",
        "descriptions": " i have been thinking about my name but i have not find it",
        "time": " 11:00 am",
        "answers":0
        }, {
            "id": 1,
            "title": "what is my name",
            "descriptions": " i have been thinking about my name but i have not find it",
            "time": " 11:00 am",
            "answers":0}]
    return question

def test_question_init():
    """check if the questions is initialized properly"""
    quiz = Question(questions_list())
    assert quiz.question_list == questions_list()

def test_question_post():
    """check if the questions are added correctly"""
    question_update = {
        "id": 1,
        "title": "I have been update",
        "descriptions": " i have been thinking about my name but i have not find it",
        "time": " 11:00 am",
        "answers":0}

    quiz = Question(questions_list())
    quiz.add_question(question_update)
    assert len(quiz.question_list) == 3

def test_update_question():
    """update the question if exists"""
    question_update = {
        "id": 1,
        "title": "I have been update",
        "descriptions": " i have been thinking about my name but i have not find it",
        "time": " 11:00 am",
        "answers":0}

    quiz = Question(questions_list())
    quiz.update_questions(0, question_update)
    assert quiz.question_list[0] == question_update

def test_delete_question():
    """check if the question has been deleted"""
    quiz = Question(questions_list())
    quiz.delete_question(0)
    assert len(quiz.question_list) == 1
