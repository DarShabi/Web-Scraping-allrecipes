import sql_connection as sq


def create_recipes_table(cursor):
    """
    Create the recipes table in the dar_maya database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
            link VARCHAR(200),
            title VARCHAR(200),
            num_reviews INT NULL,
            rating INT NULL,
            date_published DATETIME NULL
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
            FOREIGN KEY (recipe_id) REFERENCES recipes(id),
            processed BOOLEAN DEFAULT 0
        )""")


def create_ingredients_clean_table(cursor):
    """
    Create the ingredients_clean table in the database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients_clean (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            recipe_id INT, 
            ingredient VARCHAR(100), 
            quantity FLOAT
        )""")


def create_recipe_details_table(cursor):
    """
    Create the recipe_details table in the database.
    :param cursor: Cursor object used to execute the query.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_details (
            recipe_id INT PRIMARY KEY,
            prep_time_mins INT NULL,
            cook_time_mins INT NULL,
            total_time_mins INT NULL,
            servings INT NULL,
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
            calories INT NULL,
            fat_g INT NULL,
            carbs_g INT NULL,
            protein_g INT NULL,
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
            category VARCHAR(300) NULL,
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
            step INT NULL,
            description TEXT NULL,
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
    connection = sq.sql_connector("dar_maya")
    cursor = connection.cursor()

    cursor.execute('USE dar_maya')

    create_recipes_table(cursor)
    create_ingredients_table(cursor)
    create_ingredients_clean_table(cursor)
    create_recipe_details_table(cursor)
    create_nutrition_facts_table(cursor)
    create_categories_table(cursor)
    create_instructions_table(cursor)
    create_categories_recipes_table(cursor)

    # commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()


def create_db_if_nonexist():
    """Create a new dar_maya database if it doesn't already exist.
    :return: None
    """
    connection = sq.sql_connector_initial()
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS dar_maya')
    cursor.execute('USE dar_maya')
    # commit changes and close the connection
    connection.commit()
    connection.close()

