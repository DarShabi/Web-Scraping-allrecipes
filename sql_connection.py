import pymysql
import logging
import json

with open('constants.json') as f:
    constants = json.load(f)


def sql_connector_initial(database=None):
    """
    Connect to the MySQL database. This function is only called when first creating the database.
    :param database: The name of the database to connect to.
    :return: A connection object.
    """
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=constants['SQL PASSWORD'],
            database=database
        )
        return connection
    except Exception as ex:
        logging.error(f'SQL Error: could not establish an initial connection to SQL: {ex}')


def sql_connector(database='allrecipes'):
    """
    Connect to the allrecipes database.
    :param database: The name of the database to connect to.
    :return: A connection object.
    """
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='rootroot',
            database=database
        )
        return connection
    except Exception as ex:
        logging.error(f'SQL Error: could not establish a connection to SQL: {ex}')
