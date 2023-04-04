import pymysql


def sql_connector():
    """
    Connect to the MySQL database.
    :return: A connection object.
    """
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root123!',
        database='Recipes'
    )

    return connection
