'''this module is intented to do all the routing in question api'''
import time
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

@QUESTION.errorhandler(400)
def bad_request(error):
    '''return customed bad format'''
    return make_response(jsonify({"error":"the number or request you have entered is not accepted"}))

@QUESTION.errorhandler(405)
def method_not_allowed(error):
    '''return customed method not allowed'''
    return make_response(jsonify({"error":"the fthe method not allowed"}))

@QUESTION.errorhandler(410)
def deleted_nofound(error):
    '''return customed method not allowed'''
    return make_response(jsonify({"error":"the value you were lookng for has been deleted"}))


@QUESTION.route("/api/v1/questions", methods=["GET","POST"])
def home():
    """show all questions"""
    if question:
        return jsonify({"questions": question.show_questions()})
    abort(404)

@QUESTION.route('/api/v1/questions/<int:question_id>', methods=["GET"])
def get_question(question_id):
    '''get a specific question'''
    if not isinstance(question_id, int):
        abort(400)
    question_list = question.show_questions()
    my_question=[my_question for my_question in question_list if my_question["id"] == question_id]
    if my_question:
        return jsonify({"question": my_question})
    abort(404)

@QUESTION.route('/api/v1/add_question', methods=["POST"])
def post_question():
    '''post question'''
    if not request.json or not 'title' in request.json:
        abort(400)
    new_question = {
    'id': question_list[-1]['id'] + 1,
    'title': request.json['title'],
    'description': request.json['description'],
    'time': "time.time()",
    "answer": 0}
    question.add_question(new_question)
    return jsonify({'question': new_question})

@QUESTION.route('/api/v1/update_question/<int:question_id>', methods=["PUT"])
def update_question(question_id):
    '''edit question'''
    if not isinstance(question_id, int):
          abort(400)
    if not request.json:
          abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
         abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
         abort(400)
    current_question=[current_question for current_question in question_list if current_question["id"]==question_id]
    if current_question:
        title = request.json.get('title', current_question[0]["title"])
        description= request.json.get('description', current_question[0]['description'])
        time = "time.time()"
        new_question=question.update_questions(question_id, title, description, time)
        return jsonify({"question": new_question})
    abort (404)

@QUESTION.route('/api/v1/delete_question/<int:question_id>', methods=["DELETE"])
def delete_question(question_id):
    """delete question"""
    if not isinstance(question_id, int):
        abort(400)
    if question.delete_question(question_id):
        return jsonify({"result": "deleted"})
    abort(404)
