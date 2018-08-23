"""parent file for the app"""
from flask import Flask
from app.resources.questions import QUESTION
from .resources.users import users
from .resources.answers import ANSWERS
from instance.config import app_config



def create_app(config_name):
    """create APP"""
    APP=Flask(__name__, instance_relative_config=True)
    APP.register_blueprint(QUESTION)
    APP.register_blueprint(users)
    APP.register_blueprint(ANSWERS)
    APP.config.from_object(app_config[config_name])
    APP.config.from_pyfile('config.py')
    return APP
