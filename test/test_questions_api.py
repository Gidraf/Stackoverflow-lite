"""this module is intented to test all questions api"""
import pytest
import json
from flask import url_for
from flask import request
from flask import jsonify
from app import create_app
from app.questions import answer_list
from app.questions import question_list

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
          "answer": 4,
          "description": "this iis my first description",
          "id": 1,
          "time": "11:27 am",
          "title": "this is my first question?"
        },
        {
          "answer": 4,
          "description": "this iis my second description",
          "id": 2,
          "time": "11:50 am",
          "title": "this is my second question?"
        },
        {
          "answer": 4,
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
          "answer": 4,
          "answers": [
            {
              "answer_text": " this is the first answer for this answer",
              "id": 1,
              "question_id": 1,
              "time": " 11:00 am",
              "votes": 0
            },
            {
              "answer_text": " this is the second answer for this answer",
              "id": 2,
              "question_id": 1,
              "time": " 11:00 am",
              "votes": 0
            },
            {
              "answer_text": " this is the third answer for this answer",
              "id": 9,
              "question_id": 1,
              "time": " 11:00 am",
              "votes": 0
            },
            {
              "answer_text": " this is the fourth answer for this answer",
              "id": 10,
              "question_id": 1,
              "time": " 11:00 am",
              "votes": 0
            }
          ],
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
    url = 'http://localhost:5000/api/v1/add_question'
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.json == {
  "question": {
    "answer": 0,
    "description": "come on this is just a question",
    "id": 5,
    "time": "time.time()",
    "title": " this is my last question"
  }
}

    #assert response.content_type == data_type

def test_update_question(client):
        '''test if a question has been updated'''
        data_type = 'application/json'
        headers = {
            'Content-Type': data_type,
            'Accept': data_type
        }
        data = {
        "title": "this is my gidraf question",
	    "description": "helloo"
        }
        url = 'http://localhost:5000/api/v1/update_question/1'
        response = client.put(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 201

def test_delete_question(client):
    """test if a question has been deleted"""
    res=client.delete("http://localhost:5000/api/v1/delete_question/1")
    assert res.json == {
  "result": "deleted"
}


def test_post_answer(client):
    '''test if a question has been posted'''
    data_type = 'application/json'
    headers = {
        'Content-Type': data_type,
        'Accept': data_type
    }
    data = {
        "answer_text": "this is my gidraf question"
        }
    url = 'http://localhost:5000/api/v1/questions/1'
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.json == {
      "answer": {
        "answer_text": "this is my gidraf question",
        "id": 16,
        "question_id": 1,
        "time": " 11:00 am",
        "votes": 0
      }
    }
