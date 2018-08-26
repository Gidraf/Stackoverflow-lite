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
        answer_text TEXT NOT NULL,
        time_created TEXT NOT NULL,
        userid INTEGER NOT NULL,
        is_answer BOOLEAN,
        votes BIGINT,
        FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE,
        questionid INTEGER NOT NULL,
        FOREIGN KEY (questionid) REFERENCES questions(questionid) ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
        cursor = connection.cursor()
        cursor.execute(sql)

    def add_answer(self, answer_text,time_created,userid, questionid,vote,is_answer, cursor):
        """
        add answer to the database in user table
        """
        sql="""INSERT INTO answers(answer_text,time_created,userid, questionid,votes,is_answer) VALUES(%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql,(answer_text,time_created,userid, questionid,vote,is_answer))
        return cursor

    def update_answer(self, answer_text, answerid, cursor):
        """
        update answer details in the database
        """
        sql="UPDATE answers SET  answer_text=%s WHERE answerid=%s"
        self.cursor.execute(sql,(answer_text, answerid,))
        return cursor

    def delete_answer(self,answerid, cursor):
        """
        delete answer by id
        """
        sql="DELETE FROM answers WHERE answers.answerid = %s"
        cursor.execute(sql,(answerid,))
        return cursor

    def search_answer_by_questionid(self,questionid, cursor):
        """
        search answer by questionid
        """
        sql="SELECT * FROM answers WHERE questionid = %s"
        cursor.execute(sql,(questionid,))
        return cursor

    def down_vote_answer(self, answerid, vote, cursor):
        """
        donvote answers
        """
        sql="UPDATE answers SET votes+=1 WHERE answerid =%s"
        cursor.execute(sql,(vote,))
        return cursor

    def mark_prefered(self, answerid, is_answer, cursor):
        """
        mark as answer
        """
        sql="UPDATE answers SET is_answer = %s WHERE answerid = %s"
        cursor.execute(sql,(is_answer,))
        return cursor

    def search_answer_by_user(self, userid, cursor):
        """
        search answers user asked
        """
        sql="SELECT * FROM answers WHERE userid = %s"
        cursor.execute(sql,(userid,))
        return cursor

    def clear_answer_table(self, connection):
        """
        clear answer table
        """
        sql="DELETE * FROM answers"
        cursor = connection.cursor()
        cursor.execute(sql)
