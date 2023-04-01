import pymysql


def insert_recipe_data(title, ingredients, recipe_details, num_reviews, rating, nutrition_facts, date_published,
                       categories, link, instructions):
    # Connect to MySQL server
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='rootroot',
        database='recipes'
    )

    # Create cursor object
    cursor = connection.cursor()

    # Insert into recipes table
    cursor.execute("""
    INSERT INTO recipes (link, title, num_reviews, rating, date_published) VALUES (%s, %s, %s, %s, %s)""",
                   (link, title, num_reviews, rating, date_published))

    if cursor.rowcount == 0:  # if recipe was not already in the database, insert the other data

        # Get the recipe_id of the last inserted row
        recipe_id = cursor.lastrowid

        # Insert into ingredients table
        for ingredient in ingredients:
            cursor.execute("INSERT INTO ingredients (recipe_id, ingredient) VALUES (%s, %s)", (recipe_id, ingredient))

        # Insert into recipe_details table
        cursor.execute("""
        INSERT INTO recipe_details (recipe_id, prep_time_mins, cook_time_mins, total_time_mins, servings) 
        VALUES (%s, %s, %s, %s, %s)""",
                       (recipe_id, recipe_details['Prep Time:'], recipe_details['Cook Time:'],
                        recipe_details['Total Time:'], recipe_details['Servings:']))

        # Insert into nutrition_facts table
        cursor.execute("""
        INSERT INTO nutrition_facts (recipe_id, calories, fat_g, carbs_g, protein_g) VALUES (%s, %s, %s, "
                    "%s, %s)""", (recipe_id, nutrition_facts['Calories'], nutrition_facts['Fat'],
                                  nutrition_facts['Carbs'], nutrition_facts['Protein']))

        # Insert categories and their relationships
        for category in categories:
            # Check if category already exists
            cursor.execute("SELECT id FROM categories WHERE category = %s", (category,))
            category_id = cursor.fetchone()

            if category_id is None:
                # Insert new category into categories table
                cursor.execute("INSERT INTO categories (category) VALUES (%s)", (category,))
                category_id = cursor.lastrowid
            else:
                category_id = category_id[0]

            # Insert relationship
            cursor.execute("""
            INSERT INTO relationship (category_id, recipe_id) VALUES (%s, %s)", (category_id, recipe_id)""")

        # Insert into instructions table
        for step, description in instructions.items():
            cursor.execute("""
            INSERT INTO instructions (recipe_id, step, description) VALUES (%s, %s, %s)"""
                           , (recipe_id, step, description))

        connection.commit()
        cursor.close()
        connection.close()
