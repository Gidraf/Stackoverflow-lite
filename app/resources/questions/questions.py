'''this module is intented to do all the routing in question api'''
import datetime
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
from instance.config import secrets
from . import QUESTION


question=Questions()
answer=Answers()
@QUESTION.errorhandler(404)
def not_found(error):
    """customed error handler"""
    return make_response(jsonify({"error": "no item found"}),404)
@QUESTION.errorhandler(400)
def bad_request(error):
    '''return customed bad format'''
    return make_response(jsonify({"error":"the number or request you have entered is not accepted"}))

@QUESTION.route("/api/v1/questions", methods=["GET","POST"])
@jwt_required
def home():
    """show all questions"""
    try:
        questions = question.fetch_all_question()
        if questions:
            return jsonify({"questions": question.fetch_all_question()}),200
        abort(404)
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify({"error":str(error)})

@QUESTION.route('/api/v1/questions/<int:question_id>', methods=["GET","POST"])
@jwt_required
def get_question(question_id):
    '''get a specific question'''
    current_user = get_jwt_identity()
    new_question=question.search_question_by_questionid(question_id)
    if request.method == 'GET':
        try:
            return jsonify({"question":dic(new_question[0])}),200
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)})
        abort(404)
    elif request.method == "POST":
        if not request.json or not "answer_text" in request.json:
            abort(400)
        if not "userid" in request.json:
            abort(400)
        now=time.time()
        time_created=now
        answer_text=request.json["answer_text"]
        userid=request.json["userid"]
        try:
            answer.create_answer_table()
            answer.add_answer(answer_text,time_created,userid,question_id)
            question_answer=answer.search_answer_by_questionid(question_id)
            result_question=new_question[0]
            #result_question["answers"]=question_answer
            return jsonify({"question":result_question,"answers":question_answer})
        except (Exception,psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)})

@QUESTION.route('/api/v1/add_question', methods=["POST"])
@jwt_required
def post_question():
    '''post question'''
    current_user = get_jwt_identity()
    if not request.json or not 'title' in request.json:
        abort(400)
    now=time.time()
    userid=request.json["userid"]
    title= request.json['title'],
    description = request.json['description'],
    time_created = now
    try:
        question.create_question_table()
        question.add_question(title,description,time_created,userid)
        return redirect (url_for("questions.home"),200)
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify({"error":str(error)})

@QUESTION.route('/api/v1/update_question/<int:question_id>', methods=["PUT"])
@jwt_required
def update_question(question_id):
    '''edit question'''
    current_user = get_jwt_identity()
    if not request.json:
          abort(400)
    if not 'title' in request.json and type(request.json['title']) is not str:
         abort(400)
    if not 'description' in request.json and type(request.json['description']) is not str:
         abort(400)
    try:
        current_question=question.search_question_by_questionid(question_id)
        if current_question:
            title = request.json.get('title')
            description= request.json.get('description')
            question.update_question(title, description, question_id)
            return jsonify({"question":question.search_question_by_questionid(question_id)}),201
    except Exception as error:
        return jsonify({"error":str(error)})

@QUESTION.route('/api/v1/delete_question/<int:question_id>', methods=["DELETE"])
@jwt_required
def delete_question(question_id):
    """delete question"""
    current_user = get_jwt_identity()
    try:
        delete_question=question.search_question_by_questionid(question_id)
        if delete_question:
            if question.delete_question(question_id):
                return jsonify({"result": "deleted"}),200
        return jsonify({"error": "no question found"})
    except (Exception,psycopg2.DatabaseError) as error:
        return jsonify({"error": str(error)})

@QUESTION.route('/api/v1/search', methods=["GET","POST"])
@jwt_required
def search_question():
    """search question question"""
    current_user = get_jwt_identity()
    if not request.json:
          abort(400)
    if not 'title' in request.json and type(request.json['title']) != str:
         abort(400)
    key=request.json["title"]
    try:
        questions=question.search_question_by_title(key)
        if questions:
                return jsonify({"questions": questions}),200
        return jsonify({"error": "no question found"})
    except (Exception,psycopg2.DatabaseError) as error:
        return jsonify({"error": str(error)})
