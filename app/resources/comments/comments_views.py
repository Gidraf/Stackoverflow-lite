"""
comtains all the comments routing
"""
from datetime import datetime
import time
import psycopg2
import psycopg2.extras
from flask import redirect
from flask import url_for
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from app.models.answers_model import Answers
from app.models.questions_model import Questions
from app.models.comments_model import Comments
from app.models.user_model import Users
from app.models import database_connection
from . import COMMENTS
from flask_jwt_extended import jwt_required,get_jwt_identity

users = Users ()
answers = Answers()
comments = Comments()

@COMMENTS.route('/api/v1/add_comment/<int:answerid>', methods= ["POST"])
@jwt_required
def add_comment(answerid):
    """
    route for adding comment to an answer
    """
    connection = None
    try:
        connection = database_connection("development")
        if 'comment_text' not in request.json:
            return jsonify({"error":"please include answer_text"}), 400
        comment_text = request.json["comment_text"]
        if comment_text.strip():
            comments.add_comment(comment_text,answerid, connection.cursor())
            return jsonify ({"success":"comment posted"}), 201
        return jsonify({"error":"comment can't be empty"}), 400
    except Exception as error:
        return jsonify({"error":str(error)}), 400
    finally:
        if connection:
            connection.close()

@COMMENTS.route("/api/v1/comments/<int:answerid>", methods = ["GET"])
@jwt_required
def get_comments(answerid):
    """
    fetch all comments for a specific questions
    """
    connection = None
    try:
        connection = database_connection("development")
        cursor = comments.search_comment_by_answerid(answerid, connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor))
        answer_comments = cursor.fetchall()
        if answer_comments:
            return jsonify({"comments":answer_comments}), 200
        return jsonify({"error":"no comment found"}), 404
    except Exception as error:
        return jsonify({"error":str(error)}), 400

    finally:
        if connection:
            connection.close()
