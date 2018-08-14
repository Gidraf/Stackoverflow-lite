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
