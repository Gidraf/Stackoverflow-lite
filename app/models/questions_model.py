"""this model is intede to perform all the user functions"""
from . import database_connection

class Questions(object):
    """question table class"""
    def __init__(self, database_connection=database_connection()):
        """initialize the connection and cursor"""
        self.cursor=database_connection.cursor()
        self.database_connection=database_connection

    def create_question_table(self):
        "create question table"
        sql="""CREATE TABLE IF NOT EXISTS questions(
        questionid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        title VARCHAR(60) NOT NULL,
        description VARCHAR(120) NOT NULL,
        time_created TEXT NOT NULL,
        userid INTEGER NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE
        )"""
        self.cursor.execute(sql)
        self.database_connection.commit()

    def add_question(self, title, description, time_created,userid):
        "add question to the database in user table"
        sql="""INSERT INTO questions(title,description,time_created,userid) VALUES(%s,%s,%s,%s)
        """
        self.cursor.execute(sql,(title,description,time_created, userid))
        self.database_connection.commit()

    def update_question(self, title, description, questionid):
        "update question details in the database"
        sql="UPDATE questions SET title=%s, description=%s WHERE questionid=%s;"
        self.cursor.execute(sql,(title,description,questionid))
        self.database_connection.commit()

    def delete_question(self,questionid):
        "delete question by id"
        sql="DELETE FROM questions WHERE questions.questionid = %s"
        self.cursor.execute(sql,(questionid,))
        self.database_connection.commit()
        return True

    def search_question_by_title(self,title):
        "search question by title"
        sql="SELECT * FROM questions WHERE title Like %s"
        self.cursor.execute(sql,(title,))
        question=self.cursor.fetchall()
        return question

    def search_question_by_questionid(self,questionid):
        "search question by id"
        sql="SELECT * FROM questions WHERE questionid = %s"
        self.cursor.execute(sql,(questionid,))
        question=self.cursor.fetchall()
        return question

    def search_question_by_user(self,userid):
        sql="SELECT * FROM questions WHERE userid = %s"
        self.cursor.execute(sql,(userid,))
        question=self.cursor.fetchall()
        return question

    def fetch_all_question(self):
        "fetchall questions"
        sql = "SELECT * FROM questions"
        self.cursor.execute(sql)
        questions = self.cursor.fetchall()
        return questions
