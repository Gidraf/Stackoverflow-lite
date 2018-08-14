"""this module is intented to test all questions api"""
import pytest
import json
from flask import url_for
from flask import request
from flask import jsonify
from app import create_app

@pytest.fixture
def app():
    """init app"""
    app=create_app("development")
    client = app.test_client()
    return app

@pytest.fixture
def question_list():
    question_list=[{
        "id": 1,
        "title": "this is my first question?",
        "description": "this iis my first description",
        "answer": 0,
        "time": "11:27 am"}, {
            "id": 1,
            "title": "this is my second question?",
            "description": "this iis my second description",
            "answer": 1,
            "time": "11:50 am"}, {
                "id": 1,
                "title": "this is my third question?",
                "description": "this iis my third description",
                "answer": 2,
                "time": "11:50 am"}, {
                    "id": 1,
                    "title": "this is my fourth question?",
                    "description": "this iis my fourth description",
                    "answer": 3,
                    "time": "11:30 am"}]
    return question_list

def test_app(client):
    """test home page"""
    assert client.get(url_for('questions.home')).status_code == 200

def test_get_question(client):
    res = client.get(url_for("questions.home"))
    assert res.json == {
    "questions": [
        {
            "answer": 0,
            "description": "this iis my first description",
            "id": 1,
            "time": "11:27 am",
            "title": "this is my first question?"
        },
        {
            "answer": 1,
            "description": "this iis my second description",
            "id": 1,
            "time": "11:50 am",
            "title": "this is my second question?"
        },
        {
            "answer": 2,
            "description": "this iis my third description",
            "id": 1,
            "time": "11:50 am",
            "title": "this is my third question?"
        },
        {
            "answer": 3,
            "description": "this iis my fourth description",
            "id": 1,
            "time": "11:30 am",
            "title": "this is my fourth question?"
        }
    ]
}
