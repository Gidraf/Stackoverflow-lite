"""init answer views"""
from flask import Blueprint

ANSWERS=Blueprint("answers",__name__)

from . import answers_views
