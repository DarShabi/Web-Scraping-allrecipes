
import pymysql

# Connect to MySQL server
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='rootroot'
)

# Create database
cursor = connection.cursor()
cursor.execute('CREATE DATABASE recipes')


# Create the recipes table
cursor.execute("""
    CREATE TABLE recipes (
        id INT NOT NULL AUTO_INCREMENT,
        link VARCHAR(255),
        title VARCHAR(255),
        num_reviews INT,
        rating FLOAT,
        date_published DATETIME,
        prep_time_mins INT,
        cook_time_mins INT,
        total_time_mins INT,
        servings INT,
        calories INT,
        fat_g INT,
        carbs_g INT,
        protein_g INT,
        PRIMARY KEY (id)
    )
""")

# Create the ingredients table
cursor.execute("""
    CREATE TABLE ingredients (
        id INT NOT NULL AUTO_INCREMENT,
        recipe_id INT,
        ingredient VARCHAR(255),
        PRIMARY KEY (id),
        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
    )
""")

# Create the categories table
cursor.execute("""
    CREATE TABLE categories (
        id INT NOT NULL AUTO_INCREMENT,
        category VARCHAR(255),
        PRIMARY KEY (id)
    )
""")

# Create the instructions table
cursor.execute("""
    CREATE TABLE instructions (
        id INT NOT NULL AUTO_INCREMENT,
        recipe_id INT,
        step INT,
        description VARCHAR(255),
        PRIMARY KEY (id),
        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
    )
""")

# Create the recipe_category table
cursor.execute("""
    CREATE TABLE recipe_category (
        category_id INT,
        recipe_id INT,
        FOREIGN KEY (category_id) REFERENCES categories(id),
        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
    )
""")

# commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

