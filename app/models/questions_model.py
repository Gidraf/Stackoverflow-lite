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
        title VARCHAR(60) NOT NULL,
        description VARCHAR(120) NOT NULL,
        time_created TEXT NOT NULL,
        userid INTEGER NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE
        )"""
        cursor = connection.cursor()
        cursor.execute(sql)

    def add_question(self, title, description, time_created,userid, cursor):
        "add question to the database in user table"
        sql="""INSERT INTO questions(title,description,time_created,userid) VALUES(%s,%s,%s,%s)
        """
        cursor.execute(sql,(title,description,time_created, userid))
        return cursor

    def update_question(self, title, description, questionid, cursor):
        """
        update question details in the database
        """
        sql="UPDATE questions SET title=%s, description=%s WHERE questionid=%s;"
        cursor.execute(sql,(title,description,questionid))
        return cursor

    def delete_question(self,questionid,cursor):
        "delete question by id"
        sql="DELETE FROM questions WHERE questions.questionid = %s"
        cursor.execute(sql,(questionid,))
        return cursor

    def search_question_by_title(self,title,cursor):
        "search question by title"
        sql="SELECT * FROM questions WHERE title Like %s"
        cursor.execute(sql,(title,))
        return cursor

    def search_question_by_questionid(self,questionid,cursor):
        "search question by id"
        sql="SELECT * FROM questions WHERE questionid = %s"
        cursor.execute(sql,(questionid,))
        return cursor

    def search_question_by_user(self,userid, cursor):
        sql="SELECT * FROM questions WHERE userid = %s"
        cursor.execute(sql,(userid,))
        return cursor

    def fetch_all_question(self, cursor):
        "fetchall questions"
        sql = "SELECT * FROM questions"
        cursor.execute(sql)
        return cursor

    def clear_question_table(self,connection):
        "clear user table"
        sql="""DROP TABLE questions CASCADE"""
        cursor = connection.cursor()
        cursor.execute(sql)
