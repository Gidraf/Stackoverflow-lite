"""test answers model"""
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
