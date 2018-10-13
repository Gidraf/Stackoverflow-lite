"""this model is intede to perform all the user functions"""
from . import database_connection
import psycopg2

class Users(object):
    """
    user table class
    """

    def create_user_table(self, connection):
        """
        create users table
        """
        sql="""CREATE TABLE IF NOT EXISTS users(
        userid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        username VARCHAR(60) NOT NULL UNIQUE,
        useremail VARCHAR(120) NOT NULL UNIQUE,
        password VARCHAR(120) NOT NULL
        )"""
        cursor = connection.cursor()
        cursor.execute(sql)

    def register_user(self, username,email,password, cursor):
        """
        add user to the database in user table
        """
        sql="""INSERT INTO users(username,useremail,password) VALUES(%s,%s,%s)"""
        cursor.execute(sql,(username,email,password))
        return cursor

    def update_user(self, userid, username, email, password, cursor):
        """
        update user details in the database
        """
        sql="UPDATE users SET username=%s, email=%s, password=%s WHERE userid=%s"
        cursor.execute(sql,(username,email,password,userid))
        return cursor

    def delete_user(self,userid, cursor):
        """
        delete user by Id
        """
        sql="DELETE FROM users WHERE userid = %s"
        cursor.execute(sql,(userid))

    def search_user_by_username(self,username, cursor):
        """
        search user by username
        """
        sql="SELECT * FROM users WHERE UPPER(username) = UPPER(%s)"
        cursor.execute(sql,(username,))
        return cursor

    def search_user_by_email(self,useremail, cursor):
        """
        search user by email
        """
        sql = "SELECT * FROM users WHERE useremail=%s"
        cursor.execute(sql,(useremail,))
        return cursor

    def search_user_by_id(self,id, cursor):
        """
        search user by id
        """
        sql = "SELECT * FROM users WHERE userid = %s"
        cursor.execute(sql, (id,))
        return cursor


    def clear_user_table(self,connection):
        """
        clear everything in user table
        """
        sql="""DROP TABLE IF EXISTS users  CASCADE"""
        cursor = connection.cursor()
        cursor.execute(sql)
