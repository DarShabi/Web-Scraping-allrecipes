import sql_connection as sq


def create_recipes_table(cursor):
    """
    Create the recipes table in the allrecipes database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
            link VARCHAR(200),
            title VARCHAR(200),
            num_reviews INT,
            rating INT,
            date_published DATETIME
        )""")


def create_ingredients_table(cursor):
    """
    Create the ingredients table in the database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INT NOT NULL AUTO_INCREMENT,
            recipe_id INT,
            ingredient VARCHAR(500),
            PRIMARY KEY (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")


def create_recipe_details_table(cursor):
    """
    Create the recipe_details table in the database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_details (
            recipe_id INT PRIMARY KEY,
            prep_time_mins INT,
            cook_time_mins INT,
            total_time_mins INT,
            servings INT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")


def create_nutrition_facts_table(cursor):
    """
    Create the nutrition_facts table in the database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrition_facts (
            recipe_id INT PRIMARY KEY,
            calories INT,
            fat_g INT,
            carbs_g INT,
            protein_g INT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")


def create_categories_table(cursor):
    """
    Create the categories table in the database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INT NOT NULL AUTO_INCREMENT,
            category VARCHAR(300),
            PRIMARY KEY (id)
        )""")


def create_instructions_table(cursor):
    """
    Create the instructions table in the database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructions (
            id INT NOT NULL AUTO_INCREMENT,
            recipe_id INT,
            step INT,
            description TEXT,
            PRIMARY KEY (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")


def create_categories_recipes_table(cursor):
    """
    Create the categories_recipes table in the database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories_recipes (
            category_id INT,
            recipe_id INT,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")


def build_database():
    """
    Create tables for the recipes database.
    :return: None
    """
    connection = sq.sql_connector_initial(database='allrecipes')
    cursor = connection.cursor()

    cursor.execute('USE allrecipes')

    create_recipes_table(cursor)
    create_ingredients_table(cursor)
    create_recipe_details_table(cursor)
    create_nutrition_facts_table(cursor)
    create_categories_table(cursor)
    create_instructions_table(cursor)
    create_categories_recipes_table(cursor)

    # commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()


def creating_db_if_nonexist():
    """Create a new allrecipes database if it doesn't already exist.
    :return: None
    """
    connection = sq.sql_connector_initial()
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS allrecipes')
    cursor.execute('USE allrecipes')
    # commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()


def main():

    creating_db_if_nonexist()
    build_database()


if __name__ == "__main__":
    main()
