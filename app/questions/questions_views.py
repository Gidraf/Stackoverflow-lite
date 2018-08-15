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
    return make_response(jsonify({"error":"the format you have providedd is not allowed"}))

@QUESTION.errorhandler(405)
def method_not_allowed(error):
    '''return customed method not allowed'''
    return make_response(jsonify({"error":"the fthe method not allwed"}))

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
    'description': request.json.get('description', ""),
    'time': "time.time()",
    "answer": 0}
    question_list.append(new_question)
    return jsonify({'question': new_question})

@QUESTION.route('/api/v1/update_question/<int:question_id>', methods=["PUT"])
def update_question(question_id):
      '''edit question'''
      question_list=question.show_questions()
      new_question=[new_question for new_question in question_list if new_question["id"] == question_id]
      if not request.json:
          abort(400)
      if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
      if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
      if new_question:
          new_question[0]['title'] = request.json.get('title', new_question[0]['title'])
          new_question[0]['description'] = request.json.get('description', new_question[0]['description'])
          new_question[0]["time"] = "time.time()"
      return jsonify({"question": new_question[0]})
