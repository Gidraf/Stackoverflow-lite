"""initialize user blueprint"""
from flask import Blueprint

users=Blueprint("users",__name__)

from . import user_views
