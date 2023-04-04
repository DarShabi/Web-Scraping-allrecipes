import sql_connection as sq


def build_database():
    """
    Create tables for the Recipes database.
    :return: None
    """
    connection = sq.sql_connector()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE recipes (
            id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
            link VARCHAR(200),
            title VARCHAR(200),
            num_reviews INT,
            rating INT,
            date_published DATETIME
        )""")

    cursor.execute("""
        CREATE TABLE ingredients (
            id INT NOT NULL AUTO_INCREMENT,
            recipe_id INT,
            ingredient VARCHAR(500),
            PRIMARY KEY (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")

    cursor.execute("""
        CREATE TABLE recipe_details (
            recipe_id INT PRIMARY KEY,
            prep_time_mins INT,
            cook_time_mins INT,
            total_time_mins INT,
            servings INT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")

    cursor.execute("""
        CREATE TABLE nutrition_facts (
            recipe_id INT PRIMARY KEY,
            calories INT,
            fat_g INT,
            carbs_g INT,
            protein_g INT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")

    cursor.execute("""
        CREATE TABLE categories (
            id INT NOT NULL AUTO_INCREMENT,
            category VARCHAR(300),
            PRIMARY KEY (id)
        )""")

    cursor.execute("""
        CREATE TABLE instructions (
            id INT NOT NULL AUTO_INCREMENT,
            recipe_id INT,
            step INT,
            description TEXT,
            PRIMARY KEY (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")

    cursor.execute("""
        CREATE TABLE relationship (
            category_id INT,
            recipe_id INT,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )""")

    # commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()


def creating_db_if_nonexist():
    """Create a new Recipes database if it doesn't already exist.
    :return: None
    """
    connection = sq.sql_connector()
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS Recipes')
    # commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()


def main():
    creating_db_if_nonexist()
    build_database()


if __name__ == "__main__":
    main()
