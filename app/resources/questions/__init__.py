"""initialize question blueprint"""
from flask import Blueprint

QUESTION=Blueprint("questions", __name__)


from . import questions
