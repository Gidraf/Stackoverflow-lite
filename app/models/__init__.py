import psycopg2
from instance.config import params

def database_connection(connection_type):
    """
    database connection
    """
    connection=psycopg2.connect(**params)
    connection.autocommit = True
    return connection
