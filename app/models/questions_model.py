"""this model is intede to perform all the user functions"""
from . import database_connection

class Questions(object):
    """question table class"""

    def create_question_table(self,connection):
        """
        create question table
        """
        sql="""CREATE TABLE IF NOT EXISTS questions(
        questionid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        title TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        time_created TEXT NOT NULL,
        userid INTEGER NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE
        )"""
        cursor = connection.cursor()
        cursor.execute(sql)

    def add_question(self, title, description, time_created,userid, cursor):
        "add question to the database in user table"
        sql=""" INSERT INTO questions(title , description, time_created, userid) VALUES(%s, %s, %s, %s)
            """
        cursor.execute(sql,(title, description, time_created, userid))
        return cursor

    def update_question(self, title, description, questionid, cursor):
        """
        update question details in the database
        """
        sql="UPDATE questions SET title = %s, description = %s WHERE questionid = %s;"
        cursor.execute(sql,(title, description, questionid))
        return cursor

    def delete_question(self,questionid,cursor):
        """
        delete question by id
        """
        sql="DELETE FROM questions WHERE questions.questionid = %s"
        cursor.execute(sql,(questionid,))
        return cursor

    def search_question_by_full_text(self,title, cursor):
        """
        search question title full text in the database
        """
        sql="SELECT * FROM questions WHERE title = %s"
        cursor.execute(sql,(title,))
        return cursor

    def search_question_userid(self, userid, cursor):
        """
        search question of a specific user
        """
        sql = "SELECT * FROM questions WHERE userid = %s"
        cursor.execute(sql, (userid,))
        return cursor

    def search_question_by_name(self,title, cursor):
        """
        search question by string
        """
        sql="SELECT * FROM questions WHERE title ~ %s"
        cursor.execute(sql,(title,))
        return cursor

    def search_question_by_questionid(self,questionid,cursor):
        "search question by id"
        sql="""SELECT username, questionid, title, description,
        time_created,users.userid
        FROM users INNER JOIN questions
        ON users.userid = questions.userid WHERE questions.questionid = %s"""
        cursor.execute(sql,(questionid,))
        return cursor

    def fetch_all_question(self, cursor):
        "fetchall questions"
        sql = """SELECT username, questionid, title, description, time_created,
        users.userid FROM users INNER JOIN questions
        ON users.userid = questions.userid """
        cursor.execute(sql)
        return cursor

    def clear_question_table(self, connection):
        "clear user table"
        sql="""DROP TABLE IF EXISTS questions CASCADE"""
        cursor = connection.cursor()
        cursor.execute(sql)
