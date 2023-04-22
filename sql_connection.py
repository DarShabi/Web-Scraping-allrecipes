import pymysql


# CHANGE PASSWORD FOR MYSQL

def sql_connector_initial(database=None):
    """
    Connect to the MySQL database. This function is only called when first creating the database.
    :param database: The name of the database to connect to.
    :return: A connection object.
    """
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='rootroot',
        database=database
    )

    return connection


def sql_connector(database='Recipes'):
    """
    Connect to the allrecipes database.
    :param database: The name of the database to connect to.
    :return: A connection object.
    """
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root123!',
        database=database
    )

    return connection
