"""
this module contains comments class model
"""
from datetime import datetime

class Comments(object):
    """
    contains comments class model
    """

    def create_comment_table(self, connection):
        """
        create comments table
        """
        sql = """CREATE TABLE IF NOT EXISTS comments (
        comment_id SERIAL PRIMARY KEY NOT NULL UNIQUE,
        comment_text TEXT NOT NULL,
        comment_time TEXT NOT NULL,
        answerid INTEGER NOT NULL,
        userid INTEGER NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (answerid) REFERENCES answers(answerid) ON UPDATE CASCADE ON DELETE CASCADE
        )"""
        cursor = connection.cursor()
        cursor.execute(sql)

    def add_comment(self, comment_text, answerid, userid, cursor):
        """
        add comment to database
        """
        sql = """INSERT INTO comments(comment_text, answerid, comment_time, userid) VALUES(%s, %s, %s, %s)"""
        cursor.execute(sql,(comment_text, answerid, "{:%B %d, %Y}".format(datetime.utcnow()), userid))
        return cursor

    def search_comment_by_answerid(self, answerid, cursor):
        """
        search comment from the database by answerid
        """
        sql = """SELECT username, comment_time, comment_text FROM users INNER JOIN  comments ON users.userid = comments.userid WHERE comments.answerid = %s"""
        cursor.execute(sql, (answerid,))
        return cursor

    def clear_comment_table(self, connection):
        """
        drop comment table
        """
        sql = """DROP TABLE IF EXISTS comments"""
        cursor = connection.cursor()
        cursor.execute(sql)
