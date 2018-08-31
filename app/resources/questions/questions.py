'''this module is intented to do all the routing in question api'''
from datetime import datetime
import time
import psycopg2
from flask import redirect
from flask import url_for
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.questions_model import Questions
from app.models.answers_model import Answers
from app.models import database_connection
from instance.config import secrets
from . import QUESTION


question=Questions()
answer=Answers()
@QUESTION.route("/api/v1/questions", methods=["GET"])
@jwt_required
def home():
    """show all questions"""
    try:
        connection=database_connection("development")
        cursor = question.fetch_all_question(connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        questions_list=cursor.fetchall()
        if questions_list:
            return jsonify({"questions": questions_list}),200
        abort(404)
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": "request error please check your request body"}),400

@QUESTION.route('/api/v1/questions/<int:question_id>', methods=["GET"])
@jwt_required
def get_question(question_id):
    '''get a specific question'''
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")

        cursor=question.search_question_by_questionid(question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        new_question=cursor.fetchall()
        if new_question:
            return jsonify({"question":new_question[0]}),200
        return jsonify({"error":"question not found"})
        abort(404)
        connection.close()
    except Exception as e:
        return jsonify({"error": "request error please check your request body"}),400

@QUESTION.route('/api/v1/add_question', methods=["POST"])
@jwt_required
def post_question():
    '''post question'''
    try:
        current_user = get_jwt_identity()
        connection = database_connection("development")
        if not request.json or  not 'title' in request.json or not "description" in request.json :
             return jsonify({"error":"Bad request format"}),400
        userid=current_user[0]["userid"]
        title= request.json['title']
        description = request.json['description']
        time_created = datetime.utcnow()
        if title.strip() and description.strip():
            question.add_question(title,description,time_created,userid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            return jsonify({"success":"question asked"}),201
        return jsonify({"error":"bad request format"}),400
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": "Bad request format"}),400

@QUESTION.route('/api/v1/update_question/<int:question_id>', methods=["PUT"])
@jwt_required
def update_question(question_id):
    '''edit question'''
    current_user = get_jwt_identity()
    connection=database_connection("development")
    if not request.json or not 'title' in request.json \
    or not 'description' in request.json:
        return jsonify({"error":"bad request format"}),400
    try:
        cursor=question.search_question_by_questionid(question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        current_question=cursor.fetchall()
        if current_question:
            userid=current_user[0]["userid"]
            title = request.json.get('title')
            description= request.json.get('description')
            if title.strip() and description.strip():
                if userid == current_question[0]["userid"]:
                    question.update_question(title, description, question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    cursor=question.search_question_by_questionid(question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    new_question=cursor.fetchall()
                    return jsonify({"question":new_question}),200
                return jsonify({"warning":"your action cannot be completed because you don't have the right permission"})
            return jsonify({"error":"bad request format"}),400
        return jsonify({"error":"no question found"}),404
    except Exception as error:
        return jsonify({"error":"sorry your request cannot be processed"}),400

@QUESTION.route('/api/v1/delete_question/<int:question_id>', methods=["DELETE"])
@jwt_required
def delete_question(question_id):
    """delete question"""
    current_user = get_jwt_identity()
    connection=database_connection("development")
    try:
        cursor=question.search_question_by_questionid(question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        delete_question=cursor.fetchall()
        if delete_question:
            if current_user[0]["userid"] == delete_question[0]["userid"]:
                if question.delete_question(question_id,connection.cursor()):
                    return jsonify({"success": " question deleted"}),200
                return jsonify({"error": "no question found"})
            return jsonify({"warning":"your action cannot be completed because you don't have the right permission"})
        return jsonify({"error":"no question found"}),404
    except (Exception,psycopg2.DatabaseError) as error:
        return jsonify({"error": str(error)}),400
    connection.close()
