"""this module is itended to hold answers class"""
from . import  database_connection

class Answers(object):
    """
    answer table class
    """

    def create_answer_table(self,connection):
        """
        create answer table
        """
        sql="""
        CREATE TABLE IF NOT EXISTS answers(
        answerid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        answer_text TEXT UNIQUE NOT NULL,
        time_created TEXT NOT NULL,
        userid INTEGER NOT NULL,
        is_answer BOOLEAN,
        FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE,
        questionid INTEGER NOT NULL,
        FOREIGN KEY (questionid) REFERENCES questions(questionid) ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
        cursor = connection.cursor()
        cursor.execute(sql)

    def add_answer(self, answer_text,time_created,userid, questionid,is_answer, cursor):
        """
        add answer to the database in user table
        """
        sql="""
        INSERT INTO answers(answer_text,time_created,userid, questionid,is_answer) VALUES(%s,%s,%s,%s,%s)
        """
        cursor.execute(sql,(answer_text,time_created,userid, questionid,is_answer))
        get_added_answer_sql = """SELECT * FROM answers WHERE answer_text = %s """
        cursor.execute(get_added_answer_sql,(answer_text,))
        current_answer = cursor.fetchone()
        return current_answer["answerid"]

    def update_answer(self, answer_text, answerid, cursor):
        """
        update answer details in the database
        """
        sql="UPDATE answers SET  answer_text=%s WHERE answerid=%s"
        cursor.execute(sql,(answer_text, answerid,))
        return cursor

    def delete_answer(self,answerid,cursor):
        """
        delete answer from answers table
        """
        sql="DELETE FROM answers WHERE answerid = %s"
        cursor.execute(sql,(answerid,))

    def upvote_dowvote_answer(self,answerid, status, cursor):
        """
        upvote or downvote an answer
        """
        sql = None
        if status == "upvote":
            sql="UPDATE answers SET votes = votes + 1 WHERE answerid = %s"
        else:
            sql="UPDATE answers SET votes = votes - 1 WHERE answerid = %s"
        cursor.execute(sql,(answerid,))
        return cursor

    def search_answer_by_questionid(self,questionid, cursor):
        """
        search answer by questionid
        """
        sql="""SELECT username, answerid, answer_text, time_created,
        users.userid, is_answer,questionid  FROM users
         INNER JOIN answers ON users.userid = answers.userid WHERE
        answers.questionid = %s"""
        cursor.execute(sql,(questionid,))
        return cursor.fetchall()

    def search_answer_by_string(self,answer_text, cursor):
        """
        search question  by string
        """
        sql="SELECT * FROM answers WHERE answer_text = %s"
        cursor.execute(sql,(answer_text,))
        return cursor

    def mark_prefered(self, answerid, is_answer, cursor):
        """
        mark as answer
        """
        cursor.execute("UPDATE answers SET is_answer = (false) where is_answer = true")
        sql="UPDATE answers SET is_answer = %s WHERE answerid = %s"
        cursor.execute(sql,(is_answer,answerid))
        return cursor

    def search_answer_by_id(self,answerid, cursor):
        """
        search answer equal to the answer id
        """
        sql="SELECT * FROM answers WHERE answerid = %s"
        cursor.execute(sql, (answerid,))
        return cursor

    def clear_answer_table(self, connection):
        """
        clear answer table
        """
        sql="DROP TABLE IF EXISTS answers CASCADE;"
        cursor = connection.cursor()
        cursor.execute(sql)
