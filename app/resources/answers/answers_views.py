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
from app.models.answers_model import Answers
from app.models.questions_model import Questions
from app.models import database_connection
from . import ANSWERS
from flask_jwt_extended import jwt_required,get_jwt_identity

answers=Answers()
queston=Questions()
@ANSWERS.route("/api/v1/answers/<int:questionid>", methods=["GET","POST"])
@jwt_required
def question_view(questionid):
    """show all answer of a question"""
    try:
        connection=database_connection("development")
        try:
            cursor = answers.search_answer_by_questionid(questionid, connection.cursor())
            answer = cursor.fetchall()
            if answer:
                quiz=queston.search_question_by_questionid(questionid,connection.cursor())
                result={}
                result["question"]=quiz[0]
                result["answers"]=answers
                return jsonify({"answers": result}),200
            abort(404)
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)}),500
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),500

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
            cursor=answers.search_answer_by_id(answerid,connection.cursor())
            answer_list=cursor.fetchall()
            if answer_list:
                answers.update_answer(answer_text,answerid,connection.cursor())
                return jsonify({"info":"answer updated"}),200
        except Exception as error:
            return jsonify({"error": str(error)}),500
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),500

@ANSWERS.route('/api/v1/delete_answer/<int:answerid>', methods=["DELETE"])
@jwt_required
def delete_answer(answerid):
    '''delete answer'''
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")
        try:
            answers.delete_answer(answerid,connection.cursor())
            return jsonify({"info":"deleted"}),200
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)}),500
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),500

@ANSWERS.route('/api/v1/prefered_answer/<int:answerid>', methods=["PATCH"])
@jwt_required
def mark_prefered(answerid):
    """ mark answer as prefered"""
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")
        if not request.json:
            abort(400)
        if not "is_answer" in request.json:
            abort(400)
        try:
            cursor=answers.search_answer_by_id(answerid, connection.cursor())
            answer_list=cursor.fetchall()
            if answer_list:
                answers.mark_prefered(answerid, True, connection.cursor())
                answer_cursor = answer.search_answer_by_questionid(question_id,connection.cursor())
                question_answer=answer_cursor.fetchall()
                question_cursor=question.search_question_by_questionid(question_id,connection.cursor())
                new_question=question_cursor.fetchall()
                return jsonify({"question":new_question[0],"answers":question_answer}),200
            abort(404)
        except (Exception,psycopg2.DatabaseError) as error:
            return jsonify({"error": str(error)})
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),500
