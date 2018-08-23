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
from app.models.questions_model import Questions
from app.models.answers_model import Answers
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
def get_question(question_id):
    '''get a specific question'''
    if request.method == 'GET':
        try:
            new_question=question.search_question_by_questionid(question_id)
            return jsonify({"question":dic(new_question)}),200
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)})
        abort(404)
    elif request.method == "POST":
        if not request.json or not "answer_text" in request.json:
            abort(404)
        now=time.time()
        time_created=datetime.datetime.fromtimestamp(now).strftime("%D-%M-%Y %HH:%MM:%SS")
        answer_text=request.json["answer_text"]
        userid=request.json["userid"]
        try:
            answer.create_answer_table()
            answer.add_answer(answer_text,time_created,userid,question_id)
            return redirect(url_for("question_view"))
        except (Exception,psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)})

@QUESTION.route('/api/v1/add_question', methods=["POST"])
def post_question():
    '''post question'''
    if not request.json or not 'title' in request.json:
        abort(400)
    now=time.time()
    userid=request.json["userid"]
    title= request.json['title'],
    description = request.json['description'],
    time_created = datetime.datetime.fromtimestamp(now).strftime("%DD-%MM-%YY %HH:%MM:%SS")
    try:
        question.create_question_table()
        question.add_question(title,description,time_created,userid)
        return redirect (url_for("questions.home"),200)
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify({"error":str(error)})


@QUESTION.route('/api/v1/update_question/<int:question_id>', methods=["PUT"])
def update_question(question_id):
    '''edit question'''
    if not request.json:
          abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
         abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
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
def delete_question(question_id):
    """delete question"""

    try:
        delete_question=question.search_question_by_questionid(question_id)
        if delete_question:
            if question.delete_question(question_id):
                return jsonify({"result": "deleted"}),200
        return jsonify({"error": "no question found"})
    except (Exception,psycopg2.DatabaseError) as error:
        return jsonify({"error": str(error)})

@QUESTION.route('/api/v1/search', methods=["GET","POST"])
def search_question():
    """search question question"""
    if not request.json:
          abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
         abort(400)
    key=request.json["title"]
    try:
        questions=question.search_question_by_title(key)
        if questions:
                return jsonify({"questions": questions}),200
        return jsonify({"error": "no question found"})
    except (Exception,psycopg2.DatabaseError) as error:
        return jsonify({"error": str(error)})
