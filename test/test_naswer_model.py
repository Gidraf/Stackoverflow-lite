"""this model should test answer models"""
import pytest
from app.models.models import Answer



@pytest.fixture
def answer_list():
    '''answer list initialization'''
    answer_list = [{
        "id": 1,
        "answer_text": " this is the first answer for this answer",
        "time": " 11:00 am",
        "votes":0,
        "question_id": 1
        },{
            "id": 2,
            "answer_text": " this is the second answer for this answer",
            "time": " 11:00 am",
            "votes":0,
            "question_id": 1
            },{
                "id": 3,
                "answer_text": " this is the first answer for this answer",
                "time": " 11:00 am",
                "votes":0,
                "question_id": 2
                },{
                    "id": 4,
                    "answer_text": " this is the second answer for this answer",
                    "time": " 11:00 am",
                    "votes":0,
                    "question_id": 2
                    },{
                        "id": 5,
                        "answer_text": " this is the first answer for this answer",
                        "time": " 11:00 am",
                        "votes":0,
                        "question_id": 3
                        },{
                            "id": 6,
                            "answer_text": " this is the second answer for this answer",
                            "time": " 11:00 am",
                            "votes":0,
                            "question_id": 3
                            },{
                                "id": 7,
                                "answer_text": " this is the first answer for this answer",
                                "time": " 11:00 am",
                                "votes":0,
                                "question_id": 4
                                },{
                                    "id": 8,
                                    "answer_text": " this is the second answer for this answer",
                                    "time": " 11:00 am",
                                    "votes":0,
                                    "question_id": 4
                                    },{
                                        "id": 9,
                                        "answer_text": " this is the third answer for this answer",
                                        "time": " 11:00 am",
                                        "votes":0,
                                        "question_id": 1
                                        },{
                                            "id": 10,
                                            "answer_text": " this is the fourth answer for this answer",
                                            "time": " 11:00 am",
                                            "votes":0,
                                            "question_id": 1
                                            },{
                                                "id": 11,
                                                "answer_text": " this is the third answer for this answer",
                                                "time": " 11:00 am",
                                                "votes":0,
                                                "question_id": 2
                                                },{
                                                    "id": 12,
                                                    "answer_text": " this is the fourth answer for this answer",
                                                    "time": " 11:00 am",
                                                    "votes":0,
                                                    "question_id": 2
                                                    },{
                                                        "id": 13,
                                                        "answer_text": " this is the third answer for this answer",
                                                        "time": " 11:00 am",
                                                        "votes":0,
                                                        "question_id": 3
                                                        },{
                                                            "id": 14,
                                                            "answer_text": " this is the fourth answer for this answer",
                                                            "time": " 11:00 am",
                                                            "votes":0,
                                                            "question_id": 3
                                                            },{
                                                                "id": 15,
                                                                "answer_text": " this is the third answer for this answer",
                                                                "time": " 11:00 am",
                                                                "votes":0,
                                                                "question_id": 4
                                                                },]
    return answer_list

def test_answer_init():
    """check if the answer is initialized properly"""
    ans = Answer(answer_list())
    assert ans.answer_list == answer_list()

def test_answer_post():
    """check if the answers are added correctly"""
    answer_update = {
        "id": 1,
        "title": "I have been update",
        "description": " i have been thinking about my name but i have not find it",
        "time": " 11:00 am",
        "answers":0}

    ans = Answer(answer_list())
    ans.add_answer(answer_update)
    length=len(answer_list())
    assert len(ans.answer_list) == length + 1

def test_update_answer():
    """update the answer if exists"""
    answer_update = {
        "id": 2,
        "answer_text": " i have been thinking about my name but i have not find it",
        "time": " 11:00 am",
        "votes":0,
        "question_id": 1
        }

    answer_text = " i have been thinking about my name but i have not find it"
    ans = Answer(answer_list())
    result =ans.update_answer(2, answer_text)
    assert answer_update == result

def test_delete_answer():
    """check if the answer has been deleted"""
    ans = Answer(answer_list())
    deleted = ans.delete_answer(1)
    assert deleted
