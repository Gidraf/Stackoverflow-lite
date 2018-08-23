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
from . import ANSWERS

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
        answer = answers.search_answer_by_questionid(questionid)
        if answer:
            quiz=queston.search_answer_by_questionid(questionid)
            result={}
            result["question"]=quiz[0]
            result["answers"]=quiz[0]
            return jsonify({"answers": result}),200
        abort(404)
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify({"error":str(error)})

@ANSWERS.route('/api/v1/update_answer/<int:answerid>', methods=["PUT"])
def update_answer(answerid):
    """update answer"""
    if not request.json or not "answer_text" in request.json:
        abort(404)
    answerid=request.json["answerid"]
    answer_text = request.json["answer_text"]
    try:
        answer.update_answer(answerid,answer_text)
        return redirect(url_for("question_view"))
    except Exception as error:
        return jsonify({"error": str(error)})

@ANSWERS.route('/api/v1/delete_answer/<int:answerid>', methods=["DELETE"])
def delete_answer(answerid):
    '''delete answer'''
    try:
        answer.delete_answer(answerid)
        return jsonify({"info":"deleted"})
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify({"error":str(error)})

@ANSWERS.route('/api/v1/vote_answer/<int:answerid>', methods=["PUT"])
def vote_answer(answerid):
    """update answer"""
    if not request.json or not "vote" in request.json:
        abort(404)
    vote=request.json["vote"]
    try:
        answer.vote_answer(answerid,vote)
        return redirect(url_for("question_view"))
    except Exception as error:
        return jsonify({"error": str(error)})

@ANSWERS.route('/api/v1/prefered_answer/<int:answerid>', methods=["PUT"])
def mark_prefered(answerid):
    """ mark answer as prefered"""
    if not request.json or not "vote" in request.json:
        abort(400)

    is_answer=request.json["is_answer"]
    try:
        answer.mark_prefered(answerid, is_answer)
        return redirect (url_for("question_view"))
    except (Exception,psycopg2.DatabaseError) as error:
        return jsonify({"error": str(error)})
