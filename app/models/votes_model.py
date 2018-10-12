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
        answer_userid INTEGER NOT NULL,
        vote_userid INTEGER NOT NULL,
        upvote BOOLEAN NOT NULL DEFAULT False,
        FOREIGN KEY (answer_userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (answerid) REFERENCES answers(answerid) ON UPDATE CASCADE ON DELETE CASCADE
        )"""
        cursor = connection.cursor()
        cursor.execute(sql)

    def add_answers_votes(self, answerid, answer_userid, vote_userid, cursor):
        """
        initialzize votes of an answer
        """
        sql = """INSERT INTO votes (answerid, answer_userid, vote_userid) VALUES(%s, %s, %s) """
        cursor.execute(sql,(answerid, answer_userid, vote_userid))
        return cursor

    def upvote_answer(self, answersid, answer_userid, cursor):
        """
        upvote an answer
        """
        sql = """UPDATE votes SET upvote = True WHERE answerid = %s AND answer_userid = %s"""
        cursor.execute(sql, (answersid, answer_userid))
        return cursor

    def downvote_answer(self, answersid, answer_userid, cursor):
        """
        downvote an answer
        """
        sql = """UPDATE votes SET upvote = False WHERE answerid = %s AND answer_userid = %s"""
        cursor.execute(sql, (answersid, answer_userid))
        return cursor

    def search_user_vote(self, answerid, userid, cursor):
        """
        get vote of the current user
        """
        sql = """SELECT * FROM votes WHERE answerid = %s  AND vote_userid = %s """
        cursor.execute(sql,(answerid,userid ))
        return cursor.fetchone()

    def search_votes_by_answerid(self, answerid, cursor):
        """
        query votes with the same
        """
        sql = """SELECT * FROM votes WHERE answerid = %s """
        cursor.execute(sql,(answerid,))
        return cursor

    def  clear_votes_table(self, connection):
        """destroy votes table"""
        sql = """DROP TABLE IF EXISTS votes CASCADE"""
        cursor = connection.cursor()
        cursor.execute(sql)
