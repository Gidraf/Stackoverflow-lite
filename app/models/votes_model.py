"""
holds the functions and classes for votes
"""


class Votes(object):
    """
    holds downvote and upvote
    """

    def create_votes_table(self, connection):
        """
        create votes table
        """
        sql = """CREATE TABLE IF NOT EXISTS votes(
        votesid SERIAL PRIMARY KEY NOT NULL UNIQUE,
        answerid  INTEGER NOT NULL,
        userid INTEGER NOT NULL,
        upvote BOOLEAN NOT NULL DEFAULT False,
        downvote BOOLEAN NOT NULL DEFAULT False,
        FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (answerid) REFERENCES answers(answerid) ON UPDATE CASCADE ON DELETE CASCADE
        )"""
        cursor = connection.cursor()
        cursor.execute(sql)

    def add_answers_votes(self, answerid, userid, cursor):
        """
        initialzize votes of an answer
        """
        sql = """INSERT INTO votes (answerid, userid) VALUES(%s, %s) """
        cursor.execute(sql,(answerid, userid))

    def upvote_answer(self, answersid, userid, cursor):
        """
        upvote an answer
        """
        sql1 = """UPDATE votes SET downvote = False WHERE answerid = %s AND userid = %s"""
        sql = """UPDATE votes SET upvote = True WHERE answerid = %s AND userid = %s"""
        cursor.execute(sql1, (answersid, userid))
        cursor.execute(sql, (answersid,userid))
        return cursor

    def downvote_answer(self, answersid, userid, cursor):
        """
        downvote an answer
        """
        sql1 = """UPDATE votes SET upvote = False WHERE answerid = %s AND userid = %s"""
        sql = """UPDATE votes SET downvote = True WHERE answerid = %s AND userid = %s"""
        cursor.execute(sql1,(answersid, userid))
        cursor.execute(sql, (answersid,userid))
        return cursor

    def  clear_votes_table(self, connection):
        """destroy votes table"""
        sql = """DROP TABLE IF EXISTS votes"""
        cursor = connection.cursor()
        cursor.execute(sql)
