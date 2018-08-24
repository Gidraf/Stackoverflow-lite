"""this module is itended to do all the user function login"""
import psycopg2
from flask import abort
from flask import redirect
from flask import make_response
from flask import jsonify
from flask import request
import string
from flask_jwt_extended import (create_access_token,
    get_jwt_identity
)
from . import users
from app.models.user_model import Users
user = Users()

@users.errorhandler(404)
def not_found(error):
    """customed error handler"""
    return make_response(jsonify({"error": "no item found"}))

@users.errorhandler(400)
def bad_request(error):
    '''return customed bad format'''
    return make_response(jsonify({"error":"the number or request you have entered is not accepted"}))


@users.route("/auth/register", methods=["POST"])
def register():
    "register user route"
    if not request.json or not "useremail" in request.json:
        abort(404)
    if not "username" in request.json:
        abort(404)
    if not "password" in request.json:
        abort(404)
    name= request.json["username"]
    email=request.json["useremail"]
    password=request.json["password"]
    try:
        user.create_user_table()
        if user.search_user_by_email(email):
            return jsonify({"info":"email in use"})
        elif user.search_user_by_username(name):
            return jsonify({"info": "username in use"})
        user.register_user(name,email,password)
        return jsonify({"info":"user registered"}),201
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify({"error":str(error)})

@users.route ("/auth/login", methods=["POST"])
def login():
    """login users to the database"""
    if not request.json:
        abort(400)
    if not "username" in request.json:
        abort(400)
    if not "password" in request.json:
        abort(400)

    username=request.json["username"]
    password=request.json["password"]
    if not isinstance(username, (int,float)):
        character=string.punctuation
        if any(char in character  for char in username):
            return jsonify({"error":"username can't have characters"})
        try:
            current_user =user.search_user_by_username(username)
            if current_user:
                set_password=current_user[0][3]
                if str(password) == set_password:
                    token=create_access_token(identity=username)
                    return jsonify({"success":"your access token is","token":token}),200
                return jsonify({"error":current_user[0]})#jsonify({"warning":"wrong password"})
            return jsonify({"info":"no account found"})
        except (Exception,psycopg2.DatabaseError) as error:
            jsonify({"eror": error})
    return "username must be a string"
