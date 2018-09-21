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
from app.models.user_model import Users
from app.models import database_connection
from . import ANSWERS
from flask_jwt_extended import jwt_required,get_jwt_identity

users = Users()
answers=Answers()
question=Questions()
@ANSWERS.route("/api/v1/answers/<int:questionid>", methods=["POST","GET"])
@jwt_required
def question_view(questionid):
    """show all answer of a question"""
    current_user=get_jwt_identity()
    try:
        connection=database_connection("development")
        question_cursor=question.search_question_by_questionid(questionid,\
        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        quiz=question_cursor.fetchall()
        if quiz:
            if request.method == "GET":
                """get answers to a specific question"""
                cursor = answers.search_answer_by_questionid(questionid,\
                connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                question_answers = cursor.fetchall()
                if question_answers:
                    for a in question_answers:
                        user_cursor = users.search_user_by_id(a["userid"],\
                        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) )
                        username = user_cursor.fetchone()
                        a["username"] = username["username"]
                return jsonify({"question":quiz[0],"answers":question_answers}),200
            if "answer_text" not in request.json:
                return jsonify({"error":"answer_text can't be empty"}),400
            answer_text=request.json["answer_text"]
            if answer_text.strip():
                answer_cursor=answers.search_answer_by_string(answer_text,\
                connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                is_answer_available  = answer_cursor.fetchone()
                if not is_answer_available:
                    time_created=datetime.utcnow()
                    vote=0
                    is_answer=False
                    userid=current_user["userid"]
                    answers.add_answer(answer_text,time_created,userid,questionid,vote,is_answer,\
                    connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    cursor = answers.search_answer_by_questionid(questionid,\
                     connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    answers_list = cursor.fetchall()
                    result={}
                    result["question"] = quiz[0]
                    result["answers"] = answers_list
                    return jsonify(result),201
                return jsonify({"error":"answer already exists"}), 400
            return jsonify({"error":"answer cannot be empty"}),400
        return jsonify({"error":"no question found"}),404
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),400

@ANSWERS.route('/api/v1/mark_answer/<int:answerid>', methods=["PATCH"])
@jwt_required
def mark_prefered(answerid):
    """ mark answer as prefered"""
    current_user = get_jwt_identity()
    connection = database_connection("development")
    try:
        cursor=answers.search_answer_by_id(answerid, \
        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        answer_list=cursor.fetchall()
        if answer_list:
            userid=current_user["userid"]
            questionid=answer_list[0]["questionid"]
            question_cursor=question.search_question_by_questionid(questionid,\
            connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            questions_list=question_cursor.fetchall()
            if userid == questions_list[0]["userid"]:
                answers.mark_prefered(answerid, True, \
                connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                answer_cursor = answers.search_answer_by_questionid(questionid,\
                connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                question_answer=answer_cursor.fetchall()
                question_cursor=question.search_question_by_questionid(questionid,\
                connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                new_question=question_cursor.fetchall()
                return jsonify({"question":new_question[0],"answers":question_answer}),200
            return jsonify({"warning":"your action cannot be completed because you don't have the right permission"}),403
        return jsonify({"error":"answer not found"}),404
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),400

@ANSWERS.route('/api/v1/delete_answer/<int:answerid>', methods=["DELETE"])
@jwt_required
def delete_answer(answerid):
    '''delete answer'''
    current_user = get_jwt_identity()
    try:
        connection=database_connection("development")
        cursor=answers.search_answer_by_id(answerid, \
        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        answers_list=cursor.fetchall()
        if answers_list:
            answer=answers_list[0]
            question_cursor=question.search_question_by_questionid(answer["questionid"],\
            connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            questions_list=question_cursor.fetchall()
            if current_user["userid"] == answers_list[0]["userid"]:
                answers.delete_answer(answerid,\
                connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                return jsonify({"success":"deleted"}),200
            return jsonify({"warning":"your action cannot be completed \
            because you don't have the right permission"}),403
        return jsonify({"error":"Answer not found"}),404
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": str(e)}),400

@ANSWERS.route('/api/v1/update_answer/<int:answerid>', methods=["PUT"])
@jwt_required
def update_answer(answerid):
    """update answer"""
    current_user = get_jwt_identity()
    try:
        connection = database_connection("development")
        if not "answer_text" in request.json:
            return jsonify({"error":"'answer_text' key can't be found"}),400
        answer_text = request.json["answer_text"]
        if not answer_text.strip():
            return jsonify({"error":"answer text cannot be empty"}), 400
        cursor=answers.search_answer_by_id(answerid,\
        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        answer_list=cursor.fetchall()
        if answer_list:
            answer = answer_list[0]
            question_cursor=question.search_question_by_questionid(answer["questionid"],\
            connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            questions_list=question_cursor.fetchall()
            if current_user["userid"]== answer_list[0]["userid"]:
                cursor=answers.search_answer_by_string(answer_text, \
                connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                is_answer_updates_available=cursor.fetchall()
                if not is_answer_updates_available:
                    answers.update_answer(answer_text,answerid,\
                    connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    return jsonify({"success":"answer updated"}),200
                return jsonify({"error":"answer already exists"}),400
            return jsonify({"warning":"your action cannot be completed \
            because you don't have the right permission"}),403
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),400

@ANSWERS.route("/api/v1/upvote/<int:answerid>",methods=["PATCH"])
@jwt_required
def upvote_answer(answerid):
    """
    upvote answer route
    """
    current_user = get_jwt_identity()
    try:
        connection = database_connection("development")
        cursor=answers.search_answer_by_id(answerid,\
        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        answer_list=cursor.fetchall()
        if answer_list:
            answer = answer_list[0]
            answers.upvote_dowvote_answer(answerid, "upvote",\
            connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            return jsonify({"success":"answer upvoted"}),200
        return jsonify({"error":"answer not found"}),404
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),400

@ANSWERS.route("/api/v1/downvote/<int:answerid>",methods=["PATCH"])
@jwt_required
def downvote_answer(answerid):
    """
    upvote answer route
    """
    current_user = get_jwt_identity()
    try:
        connection = database_connection("development")
        cursor=answers.search_answer_by_id(answerid,\
        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        answer_list=cursor.fetchall()
        if answer_list:
            answer = answer_list[0]
            answers.upvote_dowvote_answer(answerid, "downvote",\
            connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            return jsonify({"success":"answer downvoted"}),200
        return jsonify({"error":"answer not found"}),404
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),400
