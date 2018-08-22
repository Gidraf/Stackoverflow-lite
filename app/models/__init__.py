import psycopg2
from instance.config import params


def database_connection():
    """connect to database"""
    connection=psycopg2.connect(**params)

    return connection
