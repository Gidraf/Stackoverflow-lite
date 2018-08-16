"""initialize question blueprint"""
from flask import Blueprint

QUESTION=Blueprint("questions", __name__)
question_list=[{
    "id": 1,
    "title": "this is my first question?",
    "description": "this iis my first description",
    "time": "11:27 am"}, {
        "id": 2,
        "title": "this is my second question?",
        "description": "this iis my second description",
        "answer": 1,
        "time": "11:50 am"}, {
            "id": 3,
            "title": "this is my third question?",
            "description": "this iis my third description",
            "answer": 2,
            "time": "11:50 am"}, {
                "id": 4,
                "title": "this is my fourth question?",
                "description": "this iis my fourth description",
                "answer": 3,
                "time": "11:30 am"}]

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


from . import questions_views
