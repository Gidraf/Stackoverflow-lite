"""this module is intented to test all questions api"""
import pytest
import json
from flask import url_for
from flask import request
from flask import jsonify
from app import create_app
import time

@pytest.fixture
def app():
    """init app"""
    app=create_app("testing")
    client = app.test_client()
    return app


def test_app(client):
    """test home page"""
    assert client.get(url_for('questions.home')).status_code == 200

def test_fetch_all_question_api(client):
    """
    fetch all question from the database
    """
    question_sample = {
    "title":"my question",
    "description":"this is my descriotion",
    "time_created":time.time(),
    "userid":1
    }

    response=client.get("/api/v1/questions")
    data = response.get_json("questions")
    title = data["questions"][0][1]
    assert response.status_code==200
    assert title == question_sample["title"]
