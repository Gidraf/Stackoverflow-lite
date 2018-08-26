import psycopg2
from instance.config import params
from instance.config import test_params

def database_connection(connection_type):
    """
    database connection
    """
    if connection_type == "testing":
        connection=psycopg2.connect(**test_params)
        connection.autocommit = True
        return connection
    connection=psycopg2.connect(**params)
    connection.autocommit = True
    return connection
