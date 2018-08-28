"""run app"""
from app import create_app
from app.models.answers_model import Answers
from app.models.questions_model import Questions
from app.models.user_model import Users
from app.models import database_connection

APP=create_app('development')

def Ini_init_database():
    """create database table when the app starts when the app """
    connection=database_connection("development")
    answers=Answers()
    questions=Questions()
    users=Users()
    users.create_user_table(connection)
    questions.create_question_table(connection)
    answers.create_answer_table(connection)

if __name__=="__main__":
    """run the file"""
    Ini_init_database()
    APP.run()
