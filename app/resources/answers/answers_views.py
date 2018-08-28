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

@ANSWERS.errorhandler(404)
def not_found(error):
    """customed error handler"""
    return make_response(jsonify({"error": "no item found"}),404)

@ANSWERS.errorhandler(400)
def bad_request(error):
    '''return customed bad format'''
    return make_response(jsonify({"error":"the number or request you have entered is not accepted"}))

@ANSWERS.route("/api/v1/answers/<int:questionid>", methods=["GET","POST"])
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

@ANSWERS.route('/api/v1/down_vote_answer/<int:answerid>', methods=["PUT"])
@jwt_required
def down_vote_answer(answerid):
    """update answer"""
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")
        if not request.json or not "vote" in request.json:
            abort(404)
        vote=request.json["vote"]
        if isinstance(vote, int):
            try:
                answers.vote_answer(answerid,vote, connection.cursor())
                return jsonify({"info":"voted"}),200
            except Exception as error:
                return jsonify({"error": str(error)}),500
        abort(400)
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
        try:
            cursor=answers.search_answer_by_id(answerid, connection.cursor())
            answer_list=cursor.fetchall()
            if answer_list:
                answers.mark_prefered(answerid, True, connection.cursor())
                return jsonify({"info":"success"}),200
        except (Exception,psycopg2.DatabaseError) as error:
            return jsonify({"error": str(error)})
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),500
