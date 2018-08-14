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
    app=create_app("testing")
    client = app.test_client()
    return app

def test_app(client):
    """test home page"""
    assert client.get(url_for('questions.home')).status_code == 200

def test_get_question(client):
    res = client.get(url_for("questions.home"))
    assert res.json =={
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
            "id": 2,
            "time": "11:50 am",
            "title": "this is my second question?"
        },
        {
            "answer": 2,
            "description": "this iis my third description",
            "id": 3,
            "time": "11:50 am",
            "title": "this is my third question?"
        },
        {
            "answer": 3,
            "description": "this iis my fourth description",
            "id": 4,
            "time": "11:30 am",
            "title": "this is my fourth question?"
        }
    ]
}

def test_get_specific_question(client):
    """test get a specific question"""
    res=client.get('http://localhost:5000/api/v1/questions/1')
    assert res.json == {
    "question": [
        {
            "answer": 0,
            "description": "this iis my first description",
            "id": 1,
            "time": "11:27 am",
            "title": "this is my first question?"
        }
    ]
}

def test_post_question(client):
    '''test if a question has been posted'''
    data_type = 'application/json'
    headers = {
        'Content-Type': data_type,
        'Accept': data_type
    }
    data = {
        'title':' this is my last question',
        'description': "come on this is just a question",
    }
    url = 'http://localhost:5000/api/v1/add_questions'

    response = client.post(url, data=json.dumps(data), headers=headers)

    assert response.content_type == data_type
