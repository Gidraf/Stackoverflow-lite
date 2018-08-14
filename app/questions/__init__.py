"""initialize question blueprint"""
from flask import Blueprint

QUESTION=Blueprint("questions", __name__)
question_list=[{
    "id": 1,
    "title": "this is my first question?",
    "description": "this iis my first description",
    "answer": 0,
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

from . import questions_views
