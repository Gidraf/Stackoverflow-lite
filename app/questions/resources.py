'''this module is intented to do all the routing in question api'''
import time
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from app.models.models import Question
from app.models.models import Answer
from . import QUESTION
from . import question_list
from . import answer_list

question = Question(question_list)
answer=Answer (answer_list)

@QUESTION.errorhandler(404)
def not_found(error):
    """customed error handler"""
    return make_response(jsonify({"error": "no item found"}),404)

@QUESTION.errorhandler(400)
def bad_request(error):
    '''return customed bad format'''
    return make_response(jsonify({"error":"the number or request you have entered is not accepted"}))

@QUESTION.route("/api/v1/questions", methods=["GET","POST"])
def home():
    """show all questions"""
    if question:
        for q in question.show_questions():
            #get number of answers
            q["answer"]=len(answer.show_answers(q["id"]))
        return jsonify({"questions": question.show_questions()})
    abort(404)

@QUESTION.route('/api/v1/questions/<int:question_id>', methods=["GET","POST","PUT","DELETE"])
def get_question(question_id):
    '''get a specific question'''
    if request.method == 'GET':
        question_list = question.show_questions()
        my_question=[my_question for my_question in question_list if my_question["id"] == question_id]
        if my_question:
            question_answers=answer.show_answers(my_question[0]["id"])
            my_question[0]["answers"]=question_answers
            return jsonify({"question": my_question})
        abort(404)
    elif request.method == "POST":
        if not request.json or not "answer_text" in request.json:
            abort(404)
        new_answer = {
        "id": answer_list[-1]["id"]+1,
        "answer_text": request.json["answer_text"],
        "time":" 11:00 am",
        "votes":0,
        "question_id": question_id
        }
        answer.add_answer(new_answer)
        return jsonify({"answer":new_answer})

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
    if not request.json:
          abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
         abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
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
    if question.delete_question(question_id):
        return jsonify({"result": "deleted"})
    abort(404)
