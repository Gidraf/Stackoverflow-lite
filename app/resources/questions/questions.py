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
        try:
            cursor = question.fetch_all_question(connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            questions_list=cursor.fetchall()
            if questions_list:
                return jsonify({"questions": questions_list}),200
            abort(404)
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)}),400
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
        try:
            cursor=question.search_question_by_questionid(question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            new_question=cursor.fetchall()
            if new_question:
                return jsonify({"question":new_question[0]}),200
            return jsonify({"error":"question not found"})
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)}),400
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
        if not request.json:
             return jsonify({"error":"your the content you send is empty"}),400
        if not 'title' in request.json and type(request.json['title']) != str:
             return jsonify({"error":"key error 'title' in your request"})
        if not "description" in request.json:
            return jsonify({"error":"key error 'description' in your request"})
        userid=current_user[0]["userid"]
        title= request.json['title']
        description = request.json['description']
        time_created = datetime.utcnow()
        try:
            if title.strip() and description.strip():
                question.add_question(title,description,time_created,userid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                return jsonify({"info":"question asked"}),201
            return jsonify({"error":"you have an empty key value in you body"})
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)}) #jsonify({"error": "request error please check your request body"}),400

    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": "request error please check your request body"}),400

@QUESTION.route('/api/v1/update_question/<int:question_id>', methods=["PUT"])
@jwt_required
def update_question(question_id):
    '''edit question'''
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")
        if not request.json:
             return jsonify({"error":"your the content you send is empty"}),400
        if not 'title' in request.json and type(request.json['title']) != str:
             return jsonify({"error":"key error 'title' in your request"}),400
        if not 'description' in request.json and type(request.json['description']) is not str:
              return jsonify({"error":"key error 'description' in your request"}),400
        try:
            cursor=question.search_question_by_questionid(question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            current_question=cursor.fetchall()
            if current_question:
                if current_user[0]["userid"]==current_question[0]["userid"]:
                    title = request.json.get('title')
                    description= request.json.get('description')
                    if title.strip() and description.strip():
                        question.update_question(title, description, question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                        cursor=question.search_question_by_questionid(question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                        new_question=cursor.fetchall()
                        return jsonify({"question":new_question}),200
                    return jsonify({"error":"you have an empty key value in you body"}),400
                abort(403)
            return jsonify({"error":"no question found"}),404
        except Exception as error:
            return jsonify({"error": "request error please check your request body"}),400
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"request error":"request error please check your request body"}),400

@QUESTION.route('/api/v1/delete_question/<int:question_id>', methods=["DELETE"])
@jwt_required
def delete_question(question_id):
    """delete question"""
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")
        try:
            cursor=question.search_question_by_questionid(question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            delete_question=cursor.fetchall()
            if delete_question:
                if current_user[0]["userid"] == delete_question[0]["userid"]:
                    if question.delete_question(question_id,connection.cursor()):
                        return jsonify({"result": " question deleted"}),200
                    return jsonify({"error": "no question found"})
                abort(403)
            return jsonify({"error":"no question found"}),404
        except (Exception,psycopg2.DatabaseError) as error:
            return jsonify({"error": "request error please check your request body"}),400
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": "request error please check your request body"}),400

@QUESTION.route('/api/v1/search', methods=["POST"])
@jwt_required
def search_question():
    """search question question"""
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")
        if not request.json:
             return jsonify({"error":"your the content you send is empty"}),400
        if not 'title' in request.json and type(request.json['title']) != str:
             return jsonify({"error":"key error 'title' in your request"}),400
        key=request.json["title"]

        try:
            cursor = question.search_question_by_title(key,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            questions = cursor.fetchall()
            if questions:
                    return jsonify({"questions": questions}),200
            return jsonify({"error": "no question found"}),404
        except (Exception,psycopg2.DatabaseError) as error:
            return jsonify({"error": str(error)})
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),400
