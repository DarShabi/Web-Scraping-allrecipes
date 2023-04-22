import sql_connection as sq
import logging


def is_new_recipe(cursor, title):
    check_sql = "SELECT * FROM recipes WHERE title = %s"
    check_values = (title,)
    cursor.execute(check_sql, check_values)
    result = cursor.fetchone()
    if result is None:
        return True
    else:
        return False


def insert_recipe_data(cursor, scraped_data):
    """
    Insert recipe data into the recipes table if the title does not already exist.
    :param cursor: Cursor object used to execute the query.
    :param scraped_data: A dictionary containing information about a recipe.
    :return: True if the data is inserted, False if the title already exists.
    """
    sql = "INSERT INTO recipes (id, link, title, num_reviews, rating, date_published) VALUES (NULL, %s, %s, %s, " \
          "%s, %s) "
    values = (
        scraped_data.get('link'), scraped_data.get('title'), scraped_data.get('reviews'),
        scraped_data.get('rating'),
        scraped_data.get('published'))
    cursor.execute(sql, values)


def insert_recipe_details(cursor, recipe_id, details):
    """
    Insert recipe details into the recipe_details table.
    :param cursor: Cursor object used to execute the query.
    :param recipe_id: The ID of the recipe.
    :param details: A dictionary containing the recipe details.
    """
    sql = "INSERT INTO recipe_details (recipe_id, prep_time_mins, cook_time_mins, total_time_mins, servings) " \
          "VALUES (%s, %s, %s, %s, %s)"
    values = (recipe_id, details.get('Prep Time:'), details.get('Cook Time:'), details.get('Total Time:'),
              details.get('Servings:'))
    try:
        cursor.execute(sql, values)
    except Exception as ex:
        logging.error(f'SQL Error: insert_recipe_details function: {ex}')


def insert_nutrition_facts(cursor, recipe_id, nutrition):
    """
    Insert nutrition facts into the nutrition_facts table.
    :param cursor: Cursor object used to execute the query.
    :param recipe_id: The ID of the recipe.
    :param nutrition: A dictionary containing the nutrition facts.
    """
    sql = "INSERT IGNORE INTO nutrition_facts (recipe_id, calories, fat_g, carbs_g, protein_g) " \
          "VALUES (%s, %s, %s, %s, %s)"
    values = (
        recipe_id, nutrition.get('Calories'), nutrition.get('Fat'), nutrition.get('Carbs'), nutrition.get('Protein'))
    try:
        cursor.execute(sql, values)
    except Exception as ex:
        logging.error(f'SQL Error: insert_nutrition_facts function: {ex}')


def insert_categories(cursor, recipe_id, categories):
    """
    Insert categories into the categories table and the categories_recipes table.
    :param cursor: Cursor object used to execute the query.
    :param recipe_id: The ID of the recipe.
    :param categories: A list of categories.
    """
    for category in categories:  # Check if category already exists in the categories table
        sql = "SELECT id FROM categories WHERE category=%s"
        cursor.execute(sql, (category,))
        result = cursor.fetchone()

        if not result:  # If category doesn't exist, insert it into the categories table
            sql = "INSERT INTO categories (category) VALUES (%s)"
            values = (category,)
            cursor.execute(sql, values)
            category_id = cursor.lastrowid
        else:  # If category already exists, use its ID from the categories table
            category_id = result[0]

        sql = "INSERT INTO categories_recipes (category_id, recipe_id) VALUES (%s, %s)"
        values = (category_id, recipe_id)
        try:
            cursor.execute(sql, values)
        except Exception as ex:
            logging.error(f'SQL Error: insert_categories function: {ex}')


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
        try:
            cursor.execute(sql, values)
        except Exception as ex:
            logging.error(f'SQL Error: insert_ingredients function: {ex}')


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
        try:
            cursor.execute(sql, values)
        except Exception as ex:
            logging.error(f'SQL Error: insert_instructions function: {ex}')


def write_to_database(scraped_data):
    """
    Write recipe data to the database.
    :param scraped_data: A dictionary containing information about a recipe.
    :return: None
    """
    connection = sq.sql_connector()
    cursor = connection.cursor()

    if is_new_recipe(cursor, scraped_data['title']):
        insert_recipe_data(cursor, scraped_data)
        recipe_id = cursor.lastrowid
        if scraped_data['details']:
            details = check_if_keys_exist(scraped_data['details'],
                                          ['Prep Time:', 'Cook Time:', 'Total Time:', 'Servings:'])
            insert_recipe_details(cursor, recipe_id, details)
        if scraped_data['nutrition']:
            nutrition = check_if_keys_exist(scraped_data['nutrition'], ['Calories', 'Fat', 'Carbs', 'Protein'])
            insert_nutrition_facts(cursor, recipe_id, nutrition)
        if scraped_data['category']:
            insert_categories(cursor, recipe_id, scraped_data['category'])
        if scraped_data['ingredients']:
            insert_ingredients(cursor, recipe_id, scraped_data['ingredients'])
        if scraped_data['instructions']:
            insert_instructions(cursor, recipe_id, scraped_data['instructions'])
        connection.commit()
    connection.close()


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
