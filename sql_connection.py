import pymysql
import logging
import json

with open('constants.json') as f:
    constants = json.load(f)


def sql_connector_initial():
    """
    Connect to the MySQL database.
    :return: A connection object.
    """
    try:
        connection = pymysql.connect(
            host=constants['HOST'],
            user=constants['USER'],
            password=constants['SQL PASSWORD']
        )
        return connection
    except Exception as ex:
        logging.error(f'SQL Error: could not establish a connection to SQL: {ex}')
        raise


def sql_connector(database=constants["DATABASE_NAME"]):
    """
    Connect to the MySQL database.
    :param database: The name of the database to connect to.
    :return: A connection object.
    """
    try:
        connection = pymysql.connect(
            host=constants['HOST'],
            user=constants['USER'],
            password=constants['SQL PASSWORD'],
            database=database
        )
        return connection
    except Exception as ex:
        logging.error(f'SQL Error: could not establish a connection to SQL: {ex}')
        raise
