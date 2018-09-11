"""this module is itended to do all the user function login"""
import psycopg2
import datetime
import psycopg2.extras
from flask import abort
from flask import redirect
from flask import make_response
from flask import jsonify
from flask import request
from validate_email import validate_email
import string
from flask_jwt_extended import (create_access_token,
    get_jwt_identity)
from . import users
from app.models.user_model import Users
from app.models import database_connection

user = Users()

@users.route("/auth/register", methods=["POST"])
def register():
    """
    registration of the user route
    adding user to the database
    """
    try:
        connection=database_connection("development")
        if not request.json:
             return jsonify({"error":"response body can't be empty"}),400
        if not "username" in request.json:
             return jsonify({"error":"'username' key not found"}),400
        if not "password" in request.json:
             return jsonify({"error":"'password' key not found"}),400
        if not "useremail" in request.json:
             return jsonify({"error":"'useremail' key not found"}),400
        username= request.json["username"]
        email=request.json["useremail"]
        password=request.json["password"]
        is_valid=validate_email(email)
        if not isinstance(username, (int,float)) and is_valid and password.strip():
            character=string.punctuation
            if any(char in character  for char in username) or not  username.strip():
                return jsonify({"error":"invalid username"}),400
            email_cursor = user.search_user_by_email(email,cursor=connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            username_cursor = user.search_user_by_username(username,cursor=connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            current_user_email=email_cursor.fetchone()
            current_user_username=username_cursor.fetchone()
            if current_user_email:
                return jsonify({"warning":"email already in use"}),401
            elif current_user_username:
                return jsonify({"warning": "username already in use"}),401
            user.register_user(username,email,password,cursor=connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            return jsonify({"success":"user registered"}),201
        return jsonify({"error":"invalid username or email"}),400
        connection.close
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),400

@users.route ("/auth/login", methods=["POST"])
def login():
    """
    Authenticate user based on username and password
    """
    try:
        connection=database_connection("development")
        if not request.json:
             return jsonify({"error":"response body can't be empty"}),400
        if not "username" in request.json:
             return jsonify({"error":"'username' key not found"}),400
        if not "password" in request.json:
             return jsonify({"error":"'password' key not found"}),400
        username=request.json["username"]
        password=request.json["password"]
        if not isinstance(username, (int,float)):
            character=string.punctuation
            if any(char in character  for char in username) or not\
             username.strip() or not password.strip():
                return jsonify({"error":"invalid username or password"}),400
            cursor = user.search_user_by_username(username,cursor=connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor))
            current_user = cursor.fetchone()
            if current_user:
                set_password=current_user["password"]
                if password == set_password:
                    expires = datetime.timedelta(days=1)
                    token=create_access_token(identity=current_user, expires_delta=expires)
                    return jsonify({"success":"you have been logged in","token":token}),200
                return jsonify({"error":set_password+"!=" + password}),401
            return jsonify({"info":"no account found"}),404
        connection.close()
    except Exception as e:
        return jsonify({"error": str(e)}),400
