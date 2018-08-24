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
from flask_jwt_extended import jwt_required

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
@jwt_required
def question_view(questionid):
    """show all answer of a question"""
    current_user = get_jwt_identity()
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
@jwt_required
def update_answer(answerid):
    """update answer"""
    current_user = get_jwt_identity()
    if not request.json or not "answer_text" in request.json:
        abort(404)
    answer_text = request.json["answer_text"]
    try:
        answers.update_answer(answer_text,answe)
        return jsonify({"info":"answer updated view questin to see changes made"})
    except Exception as error:
        return jsonify({"error": str(error)})

@ANSWERS.route('/api/v1/delete_answer/<int:answerid>', methods=["DELETE"])
@jwt_required
def delete_answer(answerid):
    '''delete answer'''
    current_user = get_jwt_identity()
    try:
        answers.delete_answer(answerid)
        return jsonify({"info":"deleted"})
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify({"error":str(error)})

@ANSWERS.route('/api/v1/down_vote_answer/<int:answerid>', methods=["PUT"])
@jwt_required
def down_vote_answer(answerid):
    """update answer"""
    current_user = get_jwt_identity()
    if not request.json or not "vote" in request.json:
        abort(404)
    vote=request.json["vote"]
    if isinstance(vote, int):
        try:
            answers.vote_answer(answerid,vote)
            return redirect(url_for("question_view"))
        except Exception as error:
            return jsonify({"error": str(error)})
    abort(400)

@ANSWERS.route('/api/v1/prefered_answer/<int:answerid>', methods=["GET"])
@jwt_required
def mark_prefered(answerid):
    """ mark answer as prefered"""
    current_user = get_jwt_identity()
    if not request.json or not "vote" in request.json:
        abort(400)
    is_answer=request.json["is_answer"]
    try:
        answers.mark_prefered(answerid, True)
        return redirect (url_for("question_view"))
    except (Exception,psycopg2.DatabaseError) as error:
        return jsonify({"error": str(error)})
