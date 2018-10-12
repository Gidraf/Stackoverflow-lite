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
from app.models.user_model import Users
from app.models.answers_model import Answers
from app.models.comments_model import Comments
from app.models.votes_model import Votes
from app.models import database_connection
from instance.config import secrets
from . import QUESTION


users = Users()
question = Questions()
answer = Answers()
comment = Comments()
votes = Votes()

def check_if_question_exists(title, connection):
    """
    check if the question already exists in database
    using question name
    """
    try:
        cursor = question.search_question_by_full_text(title,\
        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        available_questions = cursor.fetchone()
        if available_questions:
            if title == available_questions["title"]:
                return True
        return False
    except Exception as error:
        raise error

def update_this_question(question_id, question, title,description,connection):
    """
    should update question
    """
    question.update_question(title, description, question_id,\
    connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
    cursor=question.search_question_by_questionid(question_id,\
    connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
    new_question=cursor.fetchall()
    return jsonify({"question":new_question}),200

@QUESTION.route("/api/v1/questions", methods=["GET"])
def home():
    """show all questions"""
    try:
        connection=database_connection("development")
        answers=Answers()
        questions=Questions()
        users=Users()
        users.create_user_table(connection)
        questions.create_question_table(connection)
        answers.create_answer_table(connection)
        comment.create_comment_table(connection)
        votes.create_votes_table(connection)
        cursor = question.fetch_all_question(connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        questions_list=cursor.fetchall()
        if questions_list:
            for q in questions_list:
                answer_list  = answer.search_answer_by_questionid(q["questionid"], connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor))
                if answer_list:
                    q["answers"] = len(answer_list)
                q["answers"] = len(answer_list)
            return jsonify ({"result":questions_list}),200
        return jsonify ({"error":"No question found"}), 404
        abort(404)
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": str(e)}),400

@QUESTION.route('/api/v1/questions/<int:question_id>', methods=["GET"])
@jwt_required
def get_question(question_id):
    '''get a specific question'''
    current_user = get_jwt_identity()
    try:
        connection = database_connection("development")
        cursor=question.search_question_by_questionid(question_id,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        new_question=cursor.fetchone()
        if new_question:
            answers_list = answer.search_answer_by_questionid(new_question["questionid"],\
            connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor))
            return jsonify({"question":new_question,"answers":answers_list}),200
        return jsonify({"error":"question not found"}),404
        abort(404)
        connection.close()
    except Exception as e:
        return jsonify({"error":str(e)}),400

@QUESTION.route('/api/v1/add_question', methods=["POST"])
@jwt_required
def post_question():
    '''post question'''
    try:
        current_user = get_jwt_identity()
        connection = database_connection("development")
        if  not 'title' in request.json:
             return jsonify({"error":"title not found"}),400
        if not "description" in request.json :
            return jsonify({"error":"description not found"}),400
        userid=current_user["userid"]
        title= request.json['title']
        description = request.json['description']
        time_created = "{:%B %d, %Y}".format(datetime.utcnow())
        if title.strip() and description.strip():
            if not check_if_question_exists(title, connection):
                question.add_question(title , description, time_created,userid,connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                return jsonify({"success":"question asked"}),201
            return jsonify({"error":"question already exists"}),400
        return jsonify({"error":"invalid input, empty value are not accepted"}),400
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": str(e)}),400

@QUESTION.route('/api/v1/update_question/<int:question_id>', methods=["PUT"])
@jwt_required
def update_question(question_id):
    '''edit question'''
    current_user = get_jwt_identity()
    connection=database_connection("development")
    if not 'title' in request.json:
        return jsonify({"error":"no 'title' key found"}),400
    if not 'description' in request.json:
        return jsonify({"error":"bad request format"}),400
    try:
        cursor=question.search_question_by_questionid(question_id,\
        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        current_question = cursor.fetchall()
        if current_question:
            userid = current_user["userid"]
            title = request.json.get('title')
            description= request.json.get('description')
            if title.strip() and description.strip():
                if userid == current_question[0]["userid"]:
                    available_question_cursor = question.search_question_by_full_text(title,\
                    connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
                    is_updated_question_available = available_question_cursor.fetchone()
                    if is_updated_question_available:
                        if is_updated_question_available["questionid"] == question_id:
                            return update_this_question(question_id, question,title, description, connection)
                        return jsonify({"error":"question already exist"}),400
                    return update_this_question(question_id, question, title, description, connection)
                return jsonify({"error":"your action cannot be completed because you don't have the right permission"}),403
            return jsonify({"error":"empty value cannot be submitted"}),400
            connection.close()
        return jsonify({"error":"no question found"}),404
    except Exception as error:
        return jsonify({"error":str(error)}),400


@QUESTION.route('/api/v1/delete_question/<int:question_id>', methods=["DELETE"])
@jwt_required
def delete_question(question_id):
    """delete question"""
    current_user = get_jwt_identity()
    connection=database_connection("development")
    try:
        cursor=question.search_question_by_questionid(question_id,\
        connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
        delete_question=cursor.fetchall()
        if delete_question:
            if current_user["userid"] == delete_question[0]["userid"]:
                if question.delete_question(question_id,connection.cursor()):
                    return jsonify({"success": " question deleted"}),200
                return jsonify({"error": "no question found"}), 404
            return jsonify({"error":"your action cannot be completed because \
            you don't have the right permission"}),403
        return jsonify({"error":"no question found"}),404
    except (Exception,psycopg2.DatabaseError) as error:
        return jsonify({"error": str(error)}),400
    connection.close()
