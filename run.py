"""run app"""
from app import create_app
from flask import make_response
from flask import jsonify
from app.models.comments_model import Comments
from app.models.answers_model import Answers
from app.models.questions_model import Questions
from app.models.user_model import Users
from app.models.votes_model import Votes
from app.models import database_connection


APP=create_app('development')

@APP.errorhandler(404)
def not_found(error):
    """customed error handler"""
    return make_response(jsonify({"error": "no item found"}),404)

@APP.errorhandler(401)
def unauthorized(error):
    """customed error handler"""
    return make_response(jsonify({"error": "Please Login first"}),401)

@APP.errorhandler(405)
def bad_method(error):
    """customed error handler"""
    return make_response(jsonify({"error": "the method is not allowed"}),405)

@APP.errorhandler(500)
def internal_server(error):
    """customed error handler"""
    return make_response(jsonify({"error": "sorry technical problem occurred"}),500)

@APP.errorhandler(400)
def bad_request(error):
    '''return customed bad format'''
    return make_response(jsonify({"error":"bad request format"}))

@APP.errorhandler(403)
def bad_request(error):
    '''return customed bad format'''
    return make_response(jsonify({"error":"Permission denied"}))

def Ini_init_database():
    """create database table when the app starts when the app """
    connection=database_connection("development")
    answers=Answers()
    questions=Questions()
    users=Users()
    comment = Comments()
    votes = Votes()
    votes.create_votes_table(connection)
    comment.create_comment_table(connection)
    users.create_user_table(connection)
    questions.create_question_table(connection)
    answers.create_answer_table(connection)

if __name__=="__main__":
    """run the file"""
    Ini_init_database()
    APP.run()
