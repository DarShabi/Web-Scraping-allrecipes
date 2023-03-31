
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


# Create the Recipes table
cursor.execute('''
    CREATE TABLE Recipes (
        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        link VARCHAR(255),
        title VARCHAR(255),
        num_reviews INT,
        rating INT,
        date_published DATETIME,
        description_id INT NOT NULL,
        FOREIGN KEY(description_id) REFERENCES Descriptions(id)
    )
''')

# Create the Ingredients table
cursor.execute('''
    CREATE TABLE Ingredients (
        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        recipe_id INT NOT NULL,
        ingredient VARCHAR(255),
        FOREIGN KEY(recipe_id) REFERENCES Recipes(id)
    )
''')

# Create the Recipe_Details table
cursor.execute('''
    CREATE TABLE Recipe_Details (
        recipe_id INT PRIMARY KEY NOT NULL,
        prep_time_mins INT,
        cook_time_mins INT,
        total_time_mins INT,
        servings INT,
        FOREIGN KEY(recipe_id) REFERENCES Recipes(id)
    )
''')

# Create the Nutrition_Facts table
cursor.execute('''
    CREATE TABLE Nutrition_Facts (
        recipe_id INT PRIMARY KEY NOT NULL,
        calories INT,
        fat_g INT,
        carbs_g INT,
        protein_g INT,
        FOREIGN KEY(recipe_id) REFERENCES Recipes(id)
    )
''')

# Create the Categories table
cursor.execute('''
    CREATE TABLE Categories (
        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        category VARCHAR(255)
    )
''')

# Create the Descriptions table
cursor.execute('''
    CREATE TABLE Descriptions (
        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        description VARCHAR(255)
    )
''')

# Create the Relationship table
cursor.execute('''
    CREATE TABLE Relationship (
        category_id INT NOT NULL,
        recipe_id INT NOT NULL,
        FOREIGN KEY(category_id) REFERENCES Categories(id),
        FOREIGN KEY(recipe_id) REFERENCES Recipes(id),
        PRIMARY KEY(category_id, recipe_id)
    )
''')

connection.commit()
cursor.close()
connection.close()

