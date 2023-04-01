import pymysql


# is this supposed to work with argparse? should it be **kwargs?
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

    # Check if recipe already exists in the database
    query = "SELECT id FROM recipes WHERE title=%s"
    cursor.execute(query, title)
    result = cursor.fetchone()

    # If recipe already exists, close the connection and return
    if result:
        print(f"{title} already exists in the database.")
        cursor.close()
        connection.close()
        return

    # Insert recipe data into the recipes table
    query = "INSERT INTO recipes (title, link, num_reviews, rating, date_published, prep_time_mins, cook_time_mins, total_time_mins, servings, calories, fat_g, carbs_g, protein_g) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (title, link, num_reviews, rating, date_published, recipe_details.get('Prep Time:', None),
              recipe_details.get('Cook Time:', None), recipe_details.get('Total Time:', None), recipe_details.get('Servings:', None),
              nutrition_facts.get('Calories', None), nutrition_facts.get('Fat', None), nutrition_facts.get('Carbs', None),
              nutrition_facts.get('Protein', None))
    cursor.execute(query, values)

    # Get the recipe ID
    recipe_id = cursor.lastrowid

    # Insert ingredients into the ingredients table
    for ingredient in ingredients:
        query = "INSERT INTO ingredients (recipe_id, ingredient) VALUES (%s, %s)"
        values = (recipe_id, ingredient)
        cursor.execute(query, values)

    # Insert categories into the categories table
    category_ids = []
    for category in categories:
        query = "SELECT id FROM categories WHERE category=%s"
        cursor.execute(query, category)
        result = cursor.fetchone()

        if result:
            category_ids.append(result[0])
        else:
            query = "INSERT INTO categories (category) VALUES (%s)"
            cursor.execute(query, category)
            category_ids.append(cursor.lastrowid)

    # Insert recipe and category IDs into the recipe_category table
    for category_id in category_ids:
        query = "INSERT INTO recipe_category (category_id, recipe_id) VALUES (%s, %s)"
        values = (category_id, recipe_id)
        cursor.execute(query, values)

    # Insert instructions into the instructions table
    for step, description in instructions.items():
        query = "INSERT INTO instructions (recipe_id, step, description) VALUES (%s, %s, %s)"
        values = (recipe_id, step, description)
        cursor.execute(query, values)

    # Commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

    print(f"{title} has been added to the database.")