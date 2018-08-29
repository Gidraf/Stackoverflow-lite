'''this module is intented to do all the routing in question api'''
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
from app.models import database_connection
from . import ANSWERS
from flask_jwt_extended import jwt_required,get_jwt_identity

answers=Answers()
question=Questions()
@ANSWERS.route("/api/v1/answers/<int:questionid>", methods=["GET","POST"])
@jwt_required
def question_view(questionid):
    """show all answer of a question"""
    current_user=get_jwt_identity()
    try:
        connection=database_connection("development")

        try:
            cursor=question.search_question_by_questionid(questionid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            quiz=cursor.fetchall()
            if quiz:
                if request.method=="GET":
                    result={}
                    result["question"]=quiz[0]
                    result["answers"]=answers
                    return jsonify({"answers": result}),200
                if not request.json:
                    return jsonify({"error":"empty body"})
                if not "answer_text" in request.json:
                    return jsonify({"error":"answer_text key not found"})
                answer_text=request.json["answer_text"]
                if answer_text.strip():
                    time_created=datetime.utcnow()
                    vote=0
                    is_answer=False
                    userid=current_user[0]["userid"]
                    answers.add_answer(answer_text,time_created,userid,questionid,vote,is_answer,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    cursor = answers.search_answer_by_questionid(questionid, connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    answers_list = cursor.fetchall()
                    result={}
                    result["question"]=quiz[0]
                    result["answers"]=answers_list
                    return jsonify({"answers": result}),200
                return jsonify({"error":"answer cannot be empty"}),400
            return jsonify({"error":"question you are trying to answer is not available"}),404
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)})#jsonify({"error": "request error please check your request body"}),400
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": "request error please check your request body"}),400

@ANSWERS.route('/api/v1/update_answer/<int:answerid>', methods=["PUT"])
@jwt_required
def update_answer(answerid):
    """update answer"""
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")
        if not request.json or not "answer_text" in request.json:
            abort(404)
        answer_text = request.json["answer_text"]
        try:
            cursor=answers.search_answer_by_id(answerid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            answer_list=cursor.fetchall()
            if answer_list:
                answer=answer_list[0]
                question_cursor=question.search_question_by_questionid(answer["questionid"],connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                questions_list=question_cursor.fetchall()
                if current_user[0]["userid"]==questions_list[0]["userid"]:
                    answers.update_answer(answer_text,answerid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    return jsonify({"info":"answer updated"}),200
        except Exception as error:
            return jsonify({"error": "request error please check your request body"}),400
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": "request error please check your request body"}),400

@ANSWERS.route('/api/v1/delete_answer/<int:answerid>', methods=["DELETE"])
@jwt_required
def delete_answer(answerid):
    '''delete answer'''
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")
        try:
            cursor=answers.search_answer_by_id(answerid, connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            answers_list=cursor.fetchall()
            if answers_list:
                answer=answers_list[0]
                question_cursor=question.search_question_by_questionid(answer["questionid"],connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                questions_list=question_cursor.fetchall()
                if current_user[0]["userid"]==questions_list[0]["userid"]:
                    answers.delete_answer(answerid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    return jsonify({"info":"deleted"}),200
                abort(403)
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error": "request error please check your request body"}),400
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": "request error please check your request body"}),400

@ANSWERS.route('/api/v1/prefered_answer/<int:answerid>', methods=["PATCH"])
@jwt_required
def mark_prefered(answerid):
    """ mark answer as prefered"""
    current_user = get_jwt_identity()
    connection = database_connection("development")
    try:
        cursor=answers.search_answer_by_id(answerid, connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        answer_list=cursor.fetchall()
        if answer_list:
            questionid=answer_list[0]["questionid"]
            question_cursor=question.search_question_by_questionid(questionid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            questions_list=question_cursor.fetchall()
            if current_user[0]["userid"]==questions_list[0]["userid"]:
                answers.mark_prefered(answerid, True, connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                answer_cursor = answers.search_answer_by_questionid(questionid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                question_answer=answer_cursor.fetchall()
                question_cursor=question.search_question_by_questionid(questionid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                new_question=question_cursor.fetchall()
                return jsonify({"question":new_question[0],"answers":question_answer}),200
            abort(403)
        return jsonify({"error":"answer not found"})
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)})#jsonify({"error": "request error please check your request body"}),400
