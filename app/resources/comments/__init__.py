from flask import Blueprint


COMMENTS = Blueprint("comments",__name__)

from . import comments_views
