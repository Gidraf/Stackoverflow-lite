"""this model is intede to perform all the user functions"""
from . import database_connection
import psycopg2

class Users(object):
    """user table class"""
    def __init__(self, database_connection=database_connection()):
        """initialize the connection and cursor"""
        self.cursor=database_connection.cursor()
        self.database_connection=database_connection

    def create_user_table(self):
        "create users table"
        sql="""CREATE TABLE IF NOT EXISTS users(
        userid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        username VARCHAR(60) NOT NULL UNIQUE,
        useremail VARCHAR(120) NOT NULL UNIQUE,
        password VARCHAR(120) NOT NULL
        )"""
        self.cursor.execute(sql)
        self.database_connection.commit()

    def register_user(self, username,email,password):
        "add user to the database in user table"
        sql="""INSERT INTO users(username,useremail,password) VALUES(%s,%s,%s)"""
        self.cursor.execute(sql,(username,email,password))
        self.database_connection.commit()

    def update_user(self, userid, username, email, password):
        "update user details in the database"
        sql="UPDATE users SET username=%s, email=%s, password=%s WHERE userid=%s"
        self.cursor.execute(sql,(username,email,password,userid))
        self.cursor.close
        self.database_connection.commit()
        self.database_connection.close()

    def delete_user(self,userid):
        "delete user by Id"
        sql="DELETE FROM users WHERE userid = %s"
        self.cursor.execute(sql,(userid))
        self.database_connection.commit()

    def search_user_by_username(self,username):
        "search user by username"
        sql="SELECT * FROM users WHERE username=%s"
        self.cursor.execute(sql,(username,))
        user=self.cursor.fetchall()
        return user

    def search_user_by_email(self,useremail):
        "search user by email"
        sql = "SELECT * FROM users WHERE useremail=%s"
        self.cursor.execute(sql,(useremail,))
        user = self.cursor.fetchall()
        return user
