'''this module is intented to do all the routing in question api'''
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from app.models.models import Question
from . import QUESTION
from . import question_list

question = Question(question_list)

@QUESTION.errorhandler(404)
def not_found(error):
    """customed error handler"""
    return make_response(jsonify({"error": "no item found"}),404)

@QUESTION.route("/api/v1/questions")
def home():
    """show all questions"""
    if question:
        return jsonify({"questions": question.show_questions()})
    abort(404)
