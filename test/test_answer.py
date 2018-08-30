"""test answers model"""
import unittest
import json
from flask import url_for
from flask import request
from flask import jsonify
from app import create_app
from app.models.user_model import Users
from app.models.answers_model import Answers
from app.models.questions_model import Questions
from app.models import database_connection
from .base import BaseTest

class TestAnswer(BaseTest):
    """test answers"""

    

    def test_mark_answer_as_prefered(self):
        """test if user can answer"""
        empty={}
        url="/api/v1/prefered_answer/1"
        response=self.app.patch(url,data = json.dumps(empty), headers =self.headers)
        self.assertEqual(response.status_code,200)

    def test_display_error_message_when_posting_empty_body(self):
        """test if user can answer"""
        answer_text="hello"
        url="/api/v1/answers/1"
        response=self.app.post(url, headers =self.headers)
        self.assertEqual(response.status_code,200)
