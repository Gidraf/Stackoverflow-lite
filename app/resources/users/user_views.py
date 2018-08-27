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
from app.models import database_connection
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
    try:
        connection=database_connection("development")
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
            user.create_user_table(connection)
            email_cursor = user.search_user_by_email(email,cursor=connection.cursor())
            username_cursor = user.search_user_by_username(name,cursor=connection.cursor())
            current_user_email=email_cursor.fetchall()
            current_user_username=username_cursor.fetchall()
            if current_user_email:
                return jsonify({"info":"email in use"}),200
            elif current_user_username:
                return jsonify({"info": "username in use"}),200
            user.register_user(name,email,password,cursor=connection.cursor())
            return jsonify({"info":"user registered"}),201
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({"error":str(error)}),500
        connection.close
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),500

@users.route ("/auth/login", methods=["POST"])
def login():
    try:
        connection=database_connection("development")
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
                cursor = user.search_user_by_username(username,cursor=connection.cursor())
                current_user = cursor.fetchall()
                if current_user:
                    set_password=current_user[0][3]
                    if str(password) == set_password:
                        token=create_access_token(identity=username)
                        return jsonify({"success":"your access token is","token":token}),200
                    return jsonify({"error":"wrong password"}),400
                return jsonify({"info":"no account found"}),404
            except (Exception,psycopg2.DatabaseError) as error:
                jsonify({"eror": error}),500
        return jsonify({"error":"username must be a character"})
        connection.close()
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error":str(e)}),500