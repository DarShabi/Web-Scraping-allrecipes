import pymysql


# CHANGE PASSWORD FOR MYSQL
def sql_connector(database='allrecipes'):
    """
    Connect to the MySQL database.
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
