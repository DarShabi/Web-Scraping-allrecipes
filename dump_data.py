import sql_connection as sq


def insert_recipe_data(cursor, scraped_data):
    """
    Insert recipe data into the recipes table.
    :param cursor: Cursor object used to execute the query.
    :param scraped_data: A dictionary containing information about a recipe.
    """
    sql = "INSERT INTO recipes (link, title, num_reviews, rating, date_published) VALUES (%s, %s, %s, %s, %s)"
    values = (scraped_data['link'], scraped_data['title'], scraped_data['reviews'], scraped_data['rating'],
              scraped_data['published'])
    execute_sql(cursor, sql, values)


def insert_recipe_details(cursor, recipe_id, details):
    """
    Insert recipe details into the recipe_details table.
    :param cursor: Cursor object used to execute the query.
    :param recipe_id: The ID of the recipe.
    :param details: A dictionary containing the recipe details.
    """
    sql = "INSERT INTO recipe_details (recipe_id, prep_time_mins, cook_time_mins, total_time_mins, servings) " \
          "VALUES (%s, %s, %s, %s, %s)"
    values = (recipe_id, details['Prep Time:'], details['Cook Time:'], details['Total Time:'], details['Servings:'])
    execute_sql(cursor, sql, values)


def insert_nutrition_facts(cursor, recipe_id, nutrition):
    """
    Insert nutrition facts into the nutrition_facts table.
    :param cursor: Cursor object used to execute the query.
    :param recipe_id: The ID of the recipe.
    :param nutrition: A dictionary containing the nutrition facts.
    """
    sql = "INSERT IGNORE INTO nutrition_facts (recipe_id, calories, fat_g, carbs_g, protein_g) " \
          "VALUES (%s, %s, %s, %s, %s)"
    values = (recipe_id, nutrition['Calories'], nutrition['Fat'], nutrition['Carbs'], nutrition['Protein'])
    execute_sql(cursor, sql, values)


def insert_categories(cursor, recipe_id, categories):
    """
    Insert categories into the categories table and the relationship into the relationship table.
    :param cursor: Cursor object used to execute the query.
    :param recipe_id: The ID of the recipe.
    :param categories: A list of categories.
    """
    for category in categories:
        # Check if category already exists in the categories table
        sql = "SELECT id FROM categories WHERE category=%s"
        cursor.execute(sql, (category,))
        result = cursor.fetchone()

        if not result:
            # If category doesn't exist, insert it into the categories table
            sql = "INSERT INTO categories (category) VALUES (%s)"
            values = (category,)
            execute_sql(cursor, sql, values)
            category_id = cursor.lastrowid
        else:
            # If category already exists, use its ID from the categories table
            category_id = result[0]

        # Insert relationship between category and recipe into the relationship table
        sql = "INSERT INTO relationship (category_id, recipe_id) VALUES (%s, %s)"
        values = (category_id, recipe_id)
        execute_sql(cursor, sql, values)


def insert_ingredients(cursor, recipe_id, ingredients):
    """
    Insert ingredients into the ingredients table.
    :param cursor: Cursor object used to execute the query.
    :param recipe_id: The ID of the recipe.
    :param ingredients: A list of ingredients.
    """
    for ingredient in ingredients:
        sql = "INSERT INTO ingredients (recipe_id, ingredient) VALUES (%s, %s)"
        values = (recipe_id, ingredient)
        execute_sql(cursor, sql, values)


def insert_instructions(cursor, recipe_id, instructions):
    """
    Insert instructions into the instructions table.
    :param cursor: Cursor object used to execute the query.
    :param recipe_id: The ID of the recipe.
    :param instructions: A dictionary containing the instructions.
    """
    for step, description in instructions.items():
        sql = "INSERT INTO instructions (recipe_id, step, description) VALUES (%s, %s, %s)"
        values = (recipe_id, step, description)
        execute_sql(cursor, sql, values)


def write_to_database(scraped_data):
    """
    Write recipe data to the database.
    :param scraped_data: A dictionary containing information about a recipe.
    :return: None
    """
    connection = sq.sql_connector()
    cursor = connection.cursor()

    insert_recipe_data(cursor, scraped_data)

    # get the recipe ID from the newly inserted row
    recipe_id = cursor.lastrowid

    details_not_checked = scraped_data['details']
    details = check_if_keys_exist(details_not_checked, ['Prep Time:', 'Cook Time:', 'Total Time:', 'Servings:'])
    insert_recipe_details(cursor, recipe_id, details)

    nutrition_not_checked = scraped_data['nutrition']
    nutrition = check_if_keys_exist(nutrition_not_checked, ['Calories', 'Fat', 'Carbs', 'Protein'])
    insert_nutrition_facts(cursor, recipe_id, nutrition)

    categories = scraped_data['category']
    insert_categories(cursor, recipe_id, categories)

    ingredients = scraped_data['ingredients']
    insert_ingredients(cursor, recipe_id, ingredients)

    instructions = scraped_data['instructions']
    insert_instructions(cursor, recipe_id, instructions)

    connection.commit()
    connection.close()


def get_recipe_by_title(title):
    """
    Retrieve recipe data from the database by recipe title.
    :param title: (str) Title of the recipe to retrieve.
    :return: (tuple) A tuple containing information about the recipe, or None if not found.
    """
    connection = sq.sql_connector()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recipes WHERE title=%s", (title,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def execute_sql(cursor, sql, values):
    """
    Executes an SQL query with the given cursor, SQL statement and values.
    If an error occurs during execution, a KeyError is raised with the error message.
    :param: cursor: (cursor object) The cursor to use for executing the SQL query.
            sql: (str) The SQL statement to execute.
            values: (tuple) The values to use for the placeholders in the SQL statement.
    :return: None
    :raises KeyError: If an error occurs during execution.
    """
    try:
        cursor.execute(sql, values)
    except KeyError as ex:
        raise KeyError(f'Error executing SQL: {ex}')


def check_if_keys_exist(dict_to_check, keys_to_check):
    """
    Checks if a dictionary contains all the specified keys. If any of the keys are missing,
    they are added to the dictionary with a value of None.
    :param: dict_to_check: (dict) The dictionary to check.
            keys_to_check: (list) The list of keys to check for in the dictionary.
    :return: (dict) The dictionary with all the specified keys, with any missing keys added with a value of None.
    """
    for key in keys_to_check:
        if key not in dict_to_check:
            dict_to_check[key] = None
    return dict_to_check
