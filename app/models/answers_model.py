"""this module is itended to hold answers class"""
from . import  database_connection

class Answers(object):
    """answer table class"""

    def __init__(self, database_connection=database_connection()):
        """initialize the connection and cursor"""
        self.cursor=database_connection.cursor()
        self.database_connection=database_connection

    def create_answer_table(self):
        """create answer table"""
        sql="""CREATE TABLE IF NOT EXISTS answers(
        answerid SERIAL PRIMARY KEY UNIQUE NOT NULL,
        answer_text TEXT NOT NULL,
        time_created TEXT NOT NULL,
        userid INTEGER NOT NULL,
        is_answer BOOLEAN,
        votes BIGINT DEFAULT 0,
        FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE,
        questionid INTEGER NOT NULL,
        FOREIGN KEY (questionid) REFERENCES questions(questionid) ON UPDATE CASCADE ON DELETE CASCADE
        )"""
        self.cursor.execute(sql)
        self.database_connection.commit()

    def add_answer(self, answer_text,time_created,userid, questionid):
        """add answer to the database in user table"""
        sql="""INSERT INTO answers(answer_text,time_created,userid, questionid) VALUES(%s,%s,%s,%s)
        """
        self.cursor.execute(sql,(answer_text,time_created,userid, questionid))
        self.database_connection.commit()

    def update_answer(self, answer_text, answerid):
        "update answer details in the database"
        sql="UPDATE answers SET  answer_text=%s WHERE answerid=%s"
        self.cursor.execute(sql,(answer_text, answerid,))
        self.database_connection.commit()

    def delete_answer(self,answerid):
        "delete answer by id"
        sql="DELETE FROM answers WHERE answers.answerid = %s"
        self.cursor.execute(sql,(answerid,))
        self.database_connection.commit()
        return True

    def search_answer_by_questionid(self,questionid):
        "search answer by questionid"
        sql="SELECT * FROM answers WHERE questionid = %s"
        self.cursor.execute(sql,(questionid,))
        answer=self.cursor.fetchall()
        return answer

    def down_vote_answer(self, answerid, vote):
        """donvote answers"""
        sql="UPDATE answers SET votes+=1 WHERE answerid =%s"
        self.cursor.execute(sql,(vote,))
        self.database_connection.commit()

    def mark_prefered(self, answerid, is_answer):
        """mark as answer"""
        sql="UPDATE answers SET is_answer = %s WHERE answerid = %s"
        self.cursor.execute(sql,(is_answer,))
        self.database_connection.commit()

    def search_answer_by_user(self, userid):
        """search answers user asked"""
        sql="SELECT * FROM answers WHERE userid = %s"
        self.cursor.execute(sql,(userid,))
        answer=self.cursor.fetchall()
        return answer

    def clear_answer_table(self):
        "clear answer table"
        sql="DELETE * FROM answers"
        self.cursor.execute(sql)
        self.connection.commmit()
